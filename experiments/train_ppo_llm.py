from stable_baselines3 import PPO
from src.environment.aiops_env import AIOpsEnv
from src.utils.seeding import set_seed

SEED = 42
set_seed(SEED)

env = AIOpsEnv(use_llm_reward=True)

model = PPO(
    "MlpPolicy",
    env,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=64,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    ent_coef=0.02,
    vf_coef=0.5,
    seed=SEED,
    verbose=1
)

model.learn(total_timesteps=1000)
model.save("results/ppo/ppo_llm_reward")