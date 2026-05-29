import gymnasium as gym
from gymnasium import spaces

import numpy as np
from incidents import INCIDENTS
from actions import ACTIONS

class AIOpsEnv(gym.Env):

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

    def step(self,action):
        reward = -1
        done = False
        print(f"STEP: Taking action: {ACTIONS[action]}")
        return self._obs(),reward,done,False,{}

    def _obs(self):
        # Convert the current state to a numpy array for the observation
        print(f"OBSERVATION: {self.state}")
        return np.array([
            self.state["cpu"],
            self.state["memory"],
            self.state["latency"],
            self.state["error_rate"]
        ],dtype=np.float32)