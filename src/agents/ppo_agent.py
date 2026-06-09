# PPO Agent implementation using Stable Baselines3
from stable_baselines3 import PPO

def build_ppo(env, seed=42):
    return PPO(
        "MlpPolicy",
        env,
        seed = seed,
        learning_rate = 3e-4,
        n_steps = 2048, # rollout size, used default value
        batch_size = 64, # SGD batch size
        gamma = 0.99, # discount factor for long term reward importance
        gae_lambda = 0.95, # advantage estimation
        clip_range = 0.2, # clipping for PPO stability
        ent_coef = 0.02, # exploration factor
        vf_coef = 0.5, # value function weight
        verbose = 1
    )