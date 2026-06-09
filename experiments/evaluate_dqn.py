# Evaluate a trained DQN agent in the AIOps environment
# This script loads a trained DQN model, initializes the AIOps environment,
# and evaluates the model's performance using the Evaluator class
from stable_baselines3 import DQN
from src.environment.aiops_env import AIOpsEnv
from src.evaluation.evaluator import Evaluator
from src.utils.seeding import set_seed

set_seed(42)
env = AIOpsEnv()

model = DQN.load("results/dqn/dqn_model")
evaluator = Evaluator(env, model)
results = evaluator.evaluate()
print("\n===== DQN results =========")
print(results)
print("\n------------------")
for k, v in results.items():
    print(f"{k}: {v}")