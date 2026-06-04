from stable_baselines3 import DQN
from environment.rl_env import AIOpsEnv
import os
from dotenv import load_dotenv
load_dotenv()

# Initialize the AIOps environment
# Create the DQN model with a multi-layer perceptron policy
env = AIOpsEnv()
DQN_TIMESTEPS = int(os.getenv("DQN_TIMESTEPS", 5000))

model = DQN(
    "MlpPolicy",
    env,
    verbose = 1
)

model.learn(total_timesteps = DQN_TIMESTEPS)

model.save("models/dqn_baseline")