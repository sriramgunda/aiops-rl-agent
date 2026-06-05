# DQN Agent implementation using Stable Baselines3
from stable_baselines3 import DQN

def build_dqn(env):
    return DQN(
        "MlpPolicy",
        env,
        learning_rate = 1e-3,
        buffer_size = 10000,
        verbose = 1
    )