# This script trains a PPO agent on the AIOps environment.
# It initializes the environment, creates a PPO model, and trains it for a specified number of timesteps.
# The trained model is then saved to a file named "ppo_aiops".

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stable_baselines3 import PPO
from environment.rl_env import AIOpsEnv
from dotenv import load_dotenv
from stable_baselines3.common.callbacks import BaseCallback

load_dotenv()

# Initialize the AIOps environment
env = AIOpsEnv()
PPO_TIMESTEPS = int(os.getenv("PPO_TIMESTEPS"))
N_STEPS = int(os.getenv("PPO_N_STEPS", "2048"))
# ensure we don't request n_steps > total timesteps for quick runs
N_STEPS = max(1, min(N_STEPS, PPO_TIMESTEPS))
LEARNING_RATE = float(os.getenv("PPO_LEARNING_RATE"))
GAMMA = float(os.getenv("PPO_GAMMA"))
PPO_PRINT_FREQ = int(os.getenv("PPO_PRINT_FREQ", "1"))

# Create the PPO model with a multi-layer perceptron policy
model = PPO(
    "MlpPolicy",
    env,
    verbose = 1,
    learning_rate = LEARNING_RATE,
    gamma = GAMMA,
    n_steps = N_STEPS
)

# Train the model for a total of 10,000 timesteps
print(f"Training PPO agent for {PPO_TIMESTEPS} timesteps")
class PrintTimestepCallback(BaseCallback):
    """Callback for printing the current number of timesteps during training."""
    def __init__(self, print_freq: int = 100, verbose: int = 0):
        super().__init__(verbose)
        self.print_freq = max(1, int(print_freq))

    def _on_step(self) -> bool:
        # Called at every environment step
        if self.num_timesteps % self.print_freq == 0:
            print(f"PPO timestep: {self.num_timesteps}")
        return True

callback = PrintTimestepCallback(print_freq=PPO_PRINT_FREQ)

model.learn(
    total_timesteps = PPO_TIMESTEPS,
    callback = callback,
)

# Save the trained model to a file
model.save("models/ppo_aiops")