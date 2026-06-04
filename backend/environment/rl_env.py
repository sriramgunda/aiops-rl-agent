# This file defines the AIOpsEnv class, which is a custom environment
# for training reinforcement learning agents to handle production incidents.
# The environment simulates various types of incidents and 
# allows the agent to take actions that affect system metrics
# such as CPU usage, memory usage, latency, and error rates.
# The reward function is designed to encourage the agent
# to take effective remediation actions that improve system performance.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gymnasium as gym
from gymnasium import spaces

import numpy as np
from environment.incidents import INCIDENTS
from environment.actions import ACTIONS

from environment.dynamics import ACTION_EFFECTS
from reward_engine.hybrid_reward import hybrid_reward

class AIOpsEnv(gym.Env):
    # Define the AIOps environment for reinforcement learning.
    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(
                len(ACTIONS)
            )
        self.observation_space = spaces.Box(
                low=0,
                high=1000,
                shape=(4,),
                dtype=np.float32
            )
        self.counter = 0
        # If True, end the episode when any metric reaches 0 (stable/threshold reached)
        self.stop_on_zero = True

    # For simplicity, the reward is -1 for every step taken.
    # In a practical implementation, this would be based on the effectiveness of the action taken.
    
    def reset(self, seed = None):
        # Randomly select an incident type and return its details
        incident = np.random.choice(
            list(INCIDENTS.keys())
        )
        self.state = INCIDENTS[incident]
        print(f"RESET: Generated incident: {incident}")
        return self._obs(),{}

    def step(self, action):
        self.counter += 1
        action_name = ACTIONS[action]
        
        print(f"STEP: Action taken: {action_name}")
        print(f"STEP: Counter: {self.counter}")

        before = self.state.copy()
        self.current_incident = None
        for incident, details in INCIDENTS.items():
            if details == before:
                self.current_incident = incident
                break
        incident = self.current_incident
        transition = ACTION_EFFECTS.get(incident,{}).get(action_name,{})

        for metric in ["cpu", "memory", "latency", "error_rate"]:
            if metric in transition:
                self.state[metric] += transition[metric]

        # Clamp metrics to be non-negative
        for metric in ["cpu", "memory", "latency", "error_rate"]:
            if self.state[metric] < 0:
                self.state[metric] = 0

        after = self.state.copy()

        reward_data = hybrid_reward(
            incident,
            action_name,
            before,
            after,
            transition.get("reward", -5)
        )

        # Mark done if user-configured and any metric has reached zero
        zero_reached = any(after[m] == 0 for m in ["cpu", "memory", "latency", "error_rate"]) if self.stop_on_zero else False
        done = zero_reached or (after["error_rate"] < 10 and after["latency"] < 200)

        return self._obs(), reward_data["reward"], done, False, {}

    def _obs(self):
        # Ensure observation values are non-negative and return as numpy array
        obs = [
            max(0, self.state["cpu"]),
            max(0, self.state["memory"]),
            max(0, self.state["latency"]),
            max(0, self.state["error_rate"])
        ]
        obs_dict = {"cpu": obs[0], "memory": obs[1], "latency": obs[2], "error_rate": obs[3]}
        print(f"OBSERVATION: {obs_dict}")
        return np.array(obs, dtype=np.float32)