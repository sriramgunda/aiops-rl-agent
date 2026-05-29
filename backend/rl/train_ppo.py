# This script trains a PPO agent on the AIOps environment.
# It initializes the environment, creates a PPO model, and trains it for a specified number of timesteps.
# The trained model is then saved to a file named "ppo_aiops".

from stable_baselines3 import PPO
from environment.rl_env import AIOpsEnv

env=AIOpsEnv()
TIMESTEPS = 500

# Create the PPO model with a multi-layer perceptron policy
model=PPO(
    "MlpPolicy",
    env,
    verbose=1
)

# Train the model for a total of 10,000 timesteps
model.learn(
    total_timesteps = TIMESTEPS
)

# Save the trained model to a file
model.save("ppo_aiops")