"""Script used to play with trained agents."""
import argparse
import os
import time

import numpy as np
import yaml
from deprl import env_tonic_compat
import deprl
from matplotlib import pyplot as plt



def play_gym(agent, environment, env_args=None):
    """Launches an agent in a Gym-based environment."""
    # lambda identifier=0: environment, env_args=env_args
    # )
    observations = environment.reset()
    tendon_states = environment.tendon_states
    length = 0
    episodes = 0
    start = time.time()
    while True:
        actions = agent.test_step(observations, 1e6, tendon_states)
        observations, reward, done, infos = environment.step(actions)
        tendon_states = environment.tendon_states
        length += 1
        if done or length > 2000:
            print(f'time is {time.time() - start} for length = {length}')
            start = time.time()
            term = done
            episodes += 1
            length = 0
            observations = environment.reset()



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
    if config and hasattr(config, "env_args"):
        environment.merge_args(config.env_args)
        environment.apply_args()
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
