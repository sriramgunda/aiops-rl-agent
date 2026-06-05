# AIOps Environment for Reinforcement Learning
# This environment simulates a simplified AIOps scenario
# where an RL agent can take actions to mitigate incidents in a production environment.
import gymnasium as gym
import numpy as np

from gymnasium import spaces

from src.environment.actions import ACTIONS
from src.environment.dynamics import ACTION_EFFECTS
from src.environment.incident_generator import IncidentGenerator
from src.agents.expert_policy import EXPERT_POLICY

class AIOpsEnv(gym.Env):
    # Initialize the AIOps environment with the incident generator, action space, and observation space.
    def __init__(self):
        super().__init__()
        self.generator = IncidentGenerator()
        self.action_space = spaces.Discrete(len(ACTIONS))

        self.observation_space = spaces.Box(
            low=0,
            high=2000,
            shape=(4,),
            dtype=np.float32
        )

    # Reset the environment to an initial state by generating a new incident and returning the initial observation.
    def reset(self, seed=None, options=None):
        self.state = self.generator.generate()
        return self._obs(), {}
    
    # Step function to take an action in the environment,
    # calculate the reward based on the action effect on the incident,
    # and return the new observation, reward, done flag, and additional info.
    def step(self, action):
        action_name = ACTIONS[action]
        reward = ACTION_EFFECTS[self.state["incident"]].get(action_name, -30)

        done = True  # Each episode ends after one action for simplicity
        return (
            self._obs(),
            reward,
            done,
            False,
            {}
        )

    # Private method to convert the current state of the environment
    # into an observation vector for the RL agent.
    def _obs(self):
        return np.array([
            self.state["cpu"],
            self.state["memory"],
            self.state["latency"],
            self.state["error_rate"]
        ], dtype=np.float32)
    
    # Expert policy to determine the expected action for a given incident type,
    # which is used for evaluation purposes to compare the RL agent actions
    # against a known good policy.
    def expert_action(self, incident):
        return EXPERT_POLICY[incident]