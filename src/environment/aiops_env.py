# AIOps Environment for Reinforcement Learning
# This environment simulates a simplified AIOps scenario
# where an RL agent can take actions to mitigate incidents in a production environment.
import gymnasium as gym
import numpy as np

from gymnasium import spaces
from openai import timeout

# Import the defined actions, incident dynamics, and incident generator
from src.environment.actions import ACTIONS, ACTIONS_MAP_NUM
from src.environment.dynamics import ACTION_EFFECTS
from src.environment.incident_generator import IncidentGenerator
from src.agents.expert_policy import EXPERT_POLICY

# Retriever and RCA agent imports
from src.rag.retriever import IncidentRetriever
from src.rag.telemetry_translator import TelemetryTranslator
from src.llm.rca_agent import RCAAgent

# State builder
from src.environment.state_builder import build_state

# Import the structured reward function to calculate rewards
# based on the changes in incident metrics after taking an action.
from src.reward.structured_reward import calculate_reward

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
            # state dimesions:
            #   [cpu, memory, latency, error_rate, http_500, db_timeout,
            #   upstream_timeout, pod_restart, incident_type, confidence, recommended_action]
            shape=(11,),
            dtype=np.float32
        )

        self.max_steps = 5 # Maximum steps per episode to encourage faster resolution
        self.last_query = None
        self.last_rca = None

    # Reset the environment to an initial state by generating a new incident and returning the initial observation.
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0 # Reset step count at the beginning of each episode
        if seed is not None:
            self.generator.set_seed(seed)
        self.state = self.generator.generate()
        #self.recommend_action = ACTIONS_MAP_NUM["no_action"] # no_action = 0
        return self._obs(), {}
    
    # Step function to take an action in the environment,
    # calculate the reward based on the action effect on the incident,
    # and return the new observation, reward, done flag, and additional info.
    def step(self, action):
        action_name = ACTIONS[action]
        self.current_step += 1
        # print(f"Timestep: {self.current_step}")

        before = self.state.copy() # Store the state before taking the action to calculate reward later
        
        # Apply the action effects to the current state based on the defined dynamics
        effects = ACTION_EFFECTS.get(self.state['incident'], {}).get(action_name, {})

        for metric, change in effects.items():
            # Applied clamp to ensure metrics don't go negative
            self.state[metric] = max(0, self.state[metric] + change if metric in self.state else 0)
        
        after = self.state.copy() # State after taking the action

        # Calculate the reward
        reward = calculate_reward(before, after, self.current_step)
        confidence_factor = self.last_rca["confidence"]
        if action == self.state["recommended_action"]:
            reward += 3
        else:
            reward -= 1

        # success criteria defined, latency <= 300ms and error_rate <= 5%
        success = (self.state["latency"] <= 300 and self.state["error_rate"] <= 5)

        # timeout criteria defined as reaching the maximum number of steps without successful mitigation
        timeout = (self.current_step >= self.max_steps)

        # Episode terminates if the incident is successfully mitigated
        # or if the maximum number of steps is reached.
        done = success or timeout

        if success:
            reward += 50 # Bonus reward for successful mitigation
        
        print(f"action: {action}, recommended_action: {self.state['recommended_action']}, incident: {self.state['incident']}")

        new_observation = self._obs()
        additional_info = {
            "success":success,
            "step":self.current_step,
            "action_name": action_name,
            "current state": after,
            "next state": {
                "query": self.last_query,
                "rag result": self.last_rca
                }
            }
        print(f"info: {additional_info}")

        return (
            new_observation, # New observation after taking the action
            reward, # Reward based on the action taken
            done, # Episode ends after maximum steps
            False, # Truncated for compatibility with Gymnasium API
            additional_info # Additional info can be added here if needed
        )

    # Build the observation by retrieving relevant incident information,
    # analyzing it with the RCA agent,
    # combining it with the current metrics to create a state representation
    def _obs(self):
        query = (
            f"cpu {self.state['cpu']} "
            f"memory {self.state['memory']} "
            f"latency {self.state['latency']} "
            f"http_500 {self.state['http_500']} "
            f"db_timeout {self.state['db_timeout']} "
            f"upstream_timeout {self.state['upstream_timeout']} "
            f"pod_restart {self.state['pod_restart']}"
        )
        query = TelemetryTranslator.to_text(self.state)
        self.last_query = query
        # rag retriever to get relevant historical incidents
        retrieved = self.retriever.retrieve(query)
        # perform RCA
        rca = self.rca_agent.analyze(retrieved)
        self.last_rca = rca

        # capture the recommended action to use for next step
        #self.recommend_action = ACTIONS_MAP_NUM[rca["recommended_action"]]

        return np.array(build_state(self.state, rca), dtype=np.float32)
    
    # Expert policy to determine the expected action for a given incident type,
    # which is used for evaluation purposes to compare the RL agent actions
    # against a known good policy.
    def expert_action(self, incident):
        return EXPERT_POLICY[incident]