# PPO Agent implementation using Stable Baselines3
from stable_baselines3 import PPO

def build_ppo(env):
    return PPO(
        "MlpPolicy",
        env,
        learning_rate = 3e-4,
        gamma = 0.95,
        verbose = 1
    )