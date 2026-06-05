# Train a DQN agent in the AIOps environment
# This script initializes the AIOps environment,
# builds a DQN agent using Stable Baselines
from src.environment.aiops_env import AIOpsEnv
from src.agents.dqn_agent import build_dqn

env = AIOpsEnv()

model = build_dqn(env)
model.learn(total_timesteps = 1000)

model.save("results/dqn/dqn_model")