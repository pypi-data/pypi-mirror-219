"""Script used to play with trained agents."""
import argparse
import os

import numpy as np
import deprl  # noqa
import yaml
from deprl import env_tonic_compat
# from catatonic.utils import relabel_and_get_trifinger_reward
from matplotlib import pyplot as plt

from deprl.utils import ScoreKeeper

# from .utils import env_tonic_compat, replace_reward_trifinger


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

def play_gym(agent, environment, env_args=None):
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
        # actions[:] = -1
        observations, reward, done, infos = environment.step(actions)
        tendon_states = environment.tendon_states
        # print(actions)
        # print(observations)
        # agent.test_update(**infos, steps=steps)
        # environment.mj_render()
        # if contact:
        #     print(f'{contact=}')
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
        # clickncollect.append([observations[:, 45:69], observations[:, 69:93]])
        # score_keeper.adapt_plot(["deviation_rot", "run"])
        # score_keeper.adapt_plot(["grf", "grf"])
        # clickncollect.append([observations[:, 69:93], observations[:, 69:93]])
        # print(observations[:, 69])
        length += 1
        # print(infos['terminations'])
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
            os.makedirs('./recorded_data', exist_ok=True)
            np.save(f'./recorded_data/myoleg_efficient_joints_ep_{episodes}.npy', np.array(joints))
            np.save(f'./recorded_data/myoleg_efficient_acts_ep_{episodes}.npy', np.array(acts))
            np.save(f'./recorded_data/myoleg_efficient_grf_ep_{episodes}.npy', np.array(grf))
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
        if steps > 10000:
            if "sconegym" in str(type(environment)):
                environment.model.write_results("sconepy_example")
                break
    # print(steps)
    clickncollect = clickncollect[100:-1]
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    # print([x[1][0, 0] for x in clickncollect])
    for i in range(8):
        ax.scatter(
            [x[0][0, i * 3] for x in clickncollect],
            [x[0][0, i * 3 + 1] for x in clickncollect],
            [x[0][0, i * 3 + 2] for x in clickncollect],
            marker="x",
            color="tab:blue",
        )
        ax.scatter(
            [x[1][0, i * 3] for x in clickncollect],
            [x[1][0, i * 3 + 1] for x in clickncollect],
            [x[1][0, i * 3 + 2] for x in clickncollect],
            marker="o",
            color="tab:red",
        )
        ax.set_xlabel("X Label")
        ax.set_ylabel("Y Label")
        ax.set_zlabel("Z Label")

    plt.show()


def play_control_suite(agent, environment):
    """Launches an agent in a DeepMind Control Suite-based environment."""

    from dm_control import viewer

    class Wrapper:
        """Wrapper used to plug a Tonic environment in a dm_control viewer."""

        def __init__(self, environment):
            self.environment = environment
            self.unwrapped = environment.unwrapped
            self.action_spec = self.unwrapped.environment.action_spec
            self.physics = self.unwrapped.environment.physics
            self.infos = None
            self.steps = 0
            self.episodes = 0
            self.min_reward = float("inf")
            self.max_reward = -float("inf")
            self.global_min_reward = float("inf")
            self.global_max_reward = -float("inf")

        def reset(self):
            """Mimics a dm_control reset for the viewer."""
            self.observations = self.environment.reset()[None]
            self.tendon_states = self.environment.tendon_states

            self.score = 0
            self.length = 0
            self.min_reward = float("inf")
            self.max_reward = -float("inf")

            return self.unwrapped.last_time_step

        def step(self, actions):
            """Mimics a dm_control step for the viewer."""
            # print(actions)
            assert not np.isnan(actions.sum())
            ob, rew, term, _ = self.environment.step(actions[0])

            self.score += rew
            self.length += 1
            self.min_reward = min(self.min_reward, rew)
            self.max_reward = max(self.max_reward, rew)
            self.global_min_reward = min(self.global_min_reward, rew)
            self.global_max_reward = max(self.global_max_reward, rew)
            timeout = self.length == self.environment.max_episode_steps
            done = term or timeout

            if done:
                self.episodes += 1
                print()
                print(f"Episodes: {self.episodes:,}")
                print(f"Score: {self.score:,.3f}")
                print(f"Length: {self.length:,}")
                print(f"Terminal: {term:}")
                print(f"Min reward: {self.min_reward:,.3f}")
                print(f"Max reward: {self.max_reward:,.3f}")
                print(f"Global min reward: {self.min_reward:,.3f}")
                print(f"Global max reward: {self.max_reward:,.3f}")

            self.observations = ob[None]
            self.tendon_states = self.environment.tendon_states
            self.infos = dict(
                observations=ob[None],
                rewards=np.array([rew]),
                resets=np.array([done]),
                terminations=np.array([term]),
            )

            return self.unwrapped.last_time_step

    # Wrap the environment for the viewer.
    environment = Wrapper(environment)

    def policy(timestep):
        """Mimics a dm_control policy for the viewer."""

        if environment.infos is not None:
            agent.test_update(**environment.infos, steps=environment.steps)
            environment.steps += 1
        return agent.test_step(
            environment.observations, environment.steps, environment.tendon_states
        )
        # return agent.test_step(environment.observations, environment.steps)

    # Launch the viewer with the wrapped environment and policy.
    viewer.launch(environment, policy)


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

    # Play with the agent in the environment.
    if isinstance(environment, deprl.environments.wrappers.ActionRescaler):
        environment_type = environment.env.__class__.__name__
    else:
        environment_type = environment.__class__.__name__

    if environment_type == "ControlSuiteEnvironment":
        play_control_suite(agent, environment)
    else:
        if "Bullet" in environment_type:
            environment.render()
        if "config" in locals() and hasattr(config, "env_args"):
            play_gym(agent, environment, config.env_args)
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
