# DQN Agent implementation using Stable Baselines3
from stable_baselines3 import DQN

def build_dqn(env, seed=42):
    return DQN(
        "MlpPolicy",
        env,
        seed = seed,
        learning_rate = 1e-4,
        buffer_size = 100000, # Experience replay memory
        learning_starts = 1000,
        batch_size = 64, # Samples per gradient step
        gamma = 0.99, # discount factor, long term reward importance
        train_freq = 4,
        target_update_interval = 500,
        exploration_initial_eps = 1.0, # starts fully randomly
        exploration_final_eps = 0.05, # ends with 2% exploration
        exploration_fraction = 0.50, # exploration lasts 30% of training
        verbose = 1
    )