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

# Retriever and RCA agent imports
from src.rag.retriever import IncidentRetriever
from src.llm.rca_agent import RCAAgent
from src.environment.state_builder import build_state

class AIOpsEnv(gym.Env):
    # Initialize the AIOps environment with the incident generator, action space, and observation space.
    def __init__(self):
        super().__init__()
        self.generator = IncidentGenerator()
        self.action_space = spaces.Discrete(len(ACTIONS))

        # Initialize the retriever and RCA agent for analyzing incidents
        # and building state representations.
        self.retriever = IncidentRetriever()
        self.retriever.load("data/incidents/historical_incidents.json")
        self.rca_agent = RCAAgent()

        self.observation_space = spaces.Box(
            low=0, # Minimum values for each dimension
            high=2000, # Maximum values for each dimension
            shape=(6,), # cpu, memory, latency, error_rate, incident_type, confidence
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
            self._obs(), # New observation after taking the action
            reward, # Reward based on the action taken
            done, # Episode ends after one step for simplicity
            False, # Truncated for compatibility with Gymnasium API
            {} # Additional info can be added here if needed
        )

    # Build the observation by retrieving relevant incident information,
    # analyzing it with the RCA agent,
    # combining it with the current metrics to create a state representation
    def _obs(self):
        query = (
            f"cpu {self.state['cpu']} "
            f"memory {self.state['memory']} "
            f"latency {self.state['latency']}"
        )
        retrieved = self.retriever.retrieve(query)
        rca = self.rca_agent.analyze(retrieved)

        return np.array(build_state(self.state, rca), dtype=np.float32)
    
    # Expert policy to determine the expected action for a given incident type,
    # which is used for evaluation purposes to compare the RL agent actions
    # against a known good policy.
    def expert_action(self, incident):
        return EXPERT_POLICY[incident]