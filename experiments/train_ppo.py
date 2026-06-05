# Train a PPO agent in the AIOps environment
# This script initializes the AIOps environment,
# builds a PPO agent using Stable Baselines
from src.environment.aiops_env import AIOpsEnv
from src.agents.ppo_agent import build_ppo

env = AIOpsEnv()

model = build_ppo(env)
model.learn(total_timesteps=1000)

model.save("results/ppo/ppo_model")