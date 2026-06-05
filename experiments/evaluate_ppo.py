# Evaluate a PPO agent in the AIOps environment
# This script loads a trained PPO model, initializes the AIOps environment,
# and evaluates the agent's performance using the Evaluator class
from stable_baselines3 import PPO
from src.environment.aiops_env import AIOpsEnv
from src.evaluation.evaluator import Evaluator
env = AIOpsEnv()

model = PPO.load("results/ppo/ppo_model")
evaluator = Evaluator(env, model)
results = evaluator.evaluate()
print(results)