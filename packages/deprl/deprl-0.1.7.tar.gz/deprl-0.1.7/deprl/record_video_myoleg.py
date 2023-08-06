"""Script used to play with trained agents."""
import argparse
import os

import numpy as np
import deprl  # noqa
import yaml
from deprl import env_tonic_compat
from PIL import Image
# from catatonic.utils import relabel_and_get_trifinger_reward
from matplotlib import pyplot as plt

from deprl.utils import ScoreKeeper
from deprl.utils.utils_scone_gait_sto import new_get_avg_dtwd

# from .utils import env_tonic_compat, replace_reward_trifinger
# CAM_NAME = 'side_view'
CAM_NAME = 'front_view'

class FrameSaver:
    def __init__(self):
        self.idx = 0  
        os.makedirs('./images', exist_ok=True)
 
    def store(self, frame):
        if not self.idx % 10:
            print(f'Image {self.idx}')
        im = Image.fromarray(frame)  
        id_str = str(self.idx)   
        while len(id_str) < 5:
            id_str = '0' + id_str
        im.save(f"./images/frame_{id_str}.jpeg")
        self.idx += 1


def remove_skin(env):
    geom_1_indices = np.where(env.sim.model.geom_group == 1)
    env.sim.model.geom_rgba[geom_1_indices, 3] = 0


def apply_muscle_vis(env):
    muscle_max_force = (env.sim.model.actuator_gainprm[:, 2]-(np.min(env.sim.model.actuator_gainprm[:,2]))) / (np.max(env.sim.model.actuator_gainprm[:,2]) - np.min(env.sim.model.actuator_gainprm[:,2]))
    muscle_max_force = np.log(1.5 * muscle_max_force+3) - 0.9
    env.sim.model.tendon_width[:env.sim.model.na] = 0.01*muscle_max_force + 0.002*env.sim.data.act[:env.sim.model.na]


def get_qpos(environment, joint_name):
    adr = environment.sim.model.jnt_qposadr[
        environment.sim.model.joint_name2id(joint_name)
    ]
    return environment.sim.data.qpos[adr]


def get_grf(env):
    sensors = ['l_toes', 'r_toes', 'l_foot', 'r_foot']
    weight = np.sum(env.sim.model.body_mass[:16]) * 10
    sensor_val = np.array([env.sim.data.get_sensor(sensor) / weight for sensor in sensors])
    return sensor_val.copy()

def get_joints(env):
    joint_names = ['hip_flexion_l', 'knee_angle_l', 'ankle_angle_l', 'hip_flexion_r', 'knee_angle_r', 'ankle_angle_r']
    joint_val = np.array([get_qpos(env, joint_name) for joint_name in joint_names])
    return joint_val.copy()

def play_gym(agent, environment, env_args=None, framer=None):
    """Launches an agent in a Gym-based environment."""
    # environment = tonic.environments.distribute(
    # lambda identifier=0: environment, env_args=env_args
    # )
    observations = environment.reset()
    tendon_states = environment.tendon_states
    score_keeper = ScoreKeeper()
    score = 0
    length = 0
    min_reward = float("inf")
    max_reward = -float("inf")
    global_min_reward = float("inf")
    global_max_reward = -float("inf")
    steps = 0
    episodes = 0
    maxes = np.zeros_like(environment.action_space.shape)
    grf = []
    joints = []
    acts = []

    while True:
        actions = agent.test_step(observations, steps, tendon_states)
        frame = environment.sim.render(height=1080, width=1920, camera_name=CAM_NAME)[::-1]
        framer.store(frame)
        observations, reward, done, infos = environment.step(actions)
        tendon_states = environment.tendon_states
        if hasattr(environment.sim, "data"):
            maxes = np.maximum(maxes, environment.sim.data.qfrc_actuator)
        steps += 1
        score += reward
        if hasattr(environment, "rwd_dict"):
            grf.append(get_grf(environment))
            joints.append(get_joints(environment))
            acts.append(environment.sim.data.act.copy())
        min_reward = min(min_reward, reward)
        max_reward = max(max_reward, reward)
        global_min_reward = min(global_min_reward, reward)
        global_max_reward = max(global_max_reward, reward)
        length += 1
        if done or length >= 2000:
            term = done
            episodes += 1

            print()
            print(f"Episodes: {episodes:,}")
            print(f"Score: {score:,.3f}")
            print(f"Length: {length:,}")
            print(f"Terminal: {term:}")
            print(f"Min reward: {min_reward:,.3f}")
            print(f"Max reward: {max_reward:,.3f}")
            print(f"Global min reward: {min_reward:,.3f}")
            print(f"Global max reward: {max_reward:,.3f}")
            observations = environment.reset()
            tendon_states = environment.tendon_states
            joints, acts, grf = np.array(joints), np.array(acts), np.array(grf)

            time = np.arange(joints.shape[0]) * 0.01
            joints = np.hstack([time[:, np.newaxis], joints])
            dtwd_sum, dtwd_hip, dtwd_knee, dtwd_ankle = new_get_avg_dtwd([joints], [grf],   plot=False, convert_fn=convert_data_myoleg)
            print(f'{dtwd_sum=} {dtwd_hip=} {dtwd_knee=} {dtwd_ankle=}')
            grf = []
            joints = []
            acts = []

            score = 0
            length = 0
            success_counter = 0
            overall_success = 0
            effort = []
            min_reward = float("inf")
            max_reward = -float("inf")
            # break
        if episodes > 5:
            if "sconegym" in str(type(environment)):
                environment.model.write_results("sconepy_example")
            break


def play(path, checkpoint, seed, header, agent, environment):
    """Reloads an agent and an environment from a previous experiment."""

    checkpoint_path = None

    if path:
        deprl.logger.log(f"Loading experiment from {path}")

        # Use no checkpoint, the agent is freshly created.
        if checkpoint == "none" or agent is not None:
            deprl.logger.log("Not loading any weights")

        else:
            checkpoint_path = os.path.join(path, "checkpoints")
            if not os.path.isdir(checkpoint_path):
                deprl.logger.error(f"{checkpoint_path} is not a directory")
                checkpoint_path = None

            # List all the checkpoints.
            checkpoint_ids = []
            for file in os.listdir(checkpoint_path):
                if file[:5] == "step_":
                    checkpoint_id = file.split(".")[0]
                    checkpoint_ids.append(int(checkpoint_id[5:]))

            if checkpoint_ids:
                # Use the last checkpoint.
                if checkpoint == "last":
                    checkpoint_id = max(checkpoint_ids)
                    checkpoint_path = os.path.join(
                        checkpoint_path, f"step_{checkpoint_id}"
                    )

                # Use the specified checkpoint.
                else:
                    checkpoint_id = int(checkpoint)
                    if checkpoint_id in checkpoint_ids:
                        checkpoint_path = os.path.join(
                            checkpoint_path, f"step_{checkpoint_id}"
                        )
                    else:
                        deprl.logger.error(
                            f"Checkpoint {checkpoint_id} not found in {checkpoint_path}"
                        )
                        checkpoint_path = None

            else:
                deprl.logger.error(f"No checkpoint found in {checkpoint_path}")
                checkpoint_path = None

        # Load the experiment configuration.
        arguments_path = os.path.join(path, "config.yaml")
        with open(arguments_path, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        config = argparse.Namespace(**config)
        print(config)
        header = header or config.header
        agent = agent or config.agent
        environment = environment or config.test_environment
        environment = environment or config.environment

    # Run the header first, e.g. to load an ML framework.
    if header:
        exec(header)

    # Build the agent.
    if not agent:
        raise ValueError("No agent specified.")
    agent = eval(agent)

    # Build the environment.
    environment = env_tonic_compat(environment)()
    environment.seed(seed)

    # Adapt mpo specific settings
    if "config" in locals():
        if "mpo_args" in config:
            agent.set_params(**config.mpo_args)

    # Initialize the agent.
    agent.initialize(
        observation_space=environment.observation_space,
        action_space=environment.action_space,
        seed=seed,
    )

    # Load the weights of the agent form a checkpoint.
    if checkpoint_path:
        agent.load(checkpoint_path)

    remove_skin(environment)
    apply_muscle_vis(environment)
    frame = environment.sim.render(height=1080, width=1920, camera_name=CAM_NAME)[::-1]
    environment.sim.render_contexts[-1].vopt.flags[3] = 1
    framer = FrameSaver()
    # Play with the agent in the environment.
    if isinstance(environment, deprl.environments.wrappers.ActionRescaler):
        environment_type = environment.env.__class__.__name__
    else:
        environment_type = environment.__class__.__name__
    if "config" in locals() and hasattr(config, "env_args"):
        play_gym(agent, environment, config.env_args, framer)
    else:
        play_gym(agent, environment)


if __name__ == "__main__":
    # Argument parsing.
    parser = argparse.ArgumentParser()
    parser.add_argument("--path")
    parser.add_argument("--checkpoint", default="last")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--header")
    parser.add_argument("--agent")
    parser.add_argument("--environment", "--env")
    args = vars(parser.parse_args())
    play(**args)
