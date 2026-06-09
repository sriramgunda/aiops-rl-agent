# Train a DQN agent in the AIOps environment
# This script initializes the AIOps environment,
# builds a DQN agent using Stable Baselines
from src.environment.aiops_env import AIOpsEnv
from src.agents.dqn_agent import build_dqn
from src.callbacks.training_callback import TrainingLogger
from src.utils.seeding import set_seed


SEED = 42
set_seed(SEED)

TIMESTEPS = 1000
LOGGER_TIMESTEPS = TIMESTEPS / 10

env = AIOpsEnv()
env.reset(seed=SEED)

model = build_dqn(env, SEED)
callback = TrainingLogger(logger_timestpes = LOGGER_TIMESTEPS)
model.learn(total_timesteps = TIMESTEPS, callback=callback)

model.save("results/dqn/dqn_model")