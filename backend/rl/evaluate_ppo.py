# This script evaluates the performance of the trained PPO model
# on the AIOps environment. It runs multiple episodes and calculates the success rate.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from stable_baselines3 import PPO
from environment.rl_env import AIOpsEnv

env = AIOpsEnv()
model = PPO.load("models/ppo_aiops")

episodes = 10
success = 0

for episode in range(episodes):
    print(f"Evaluate PPO: Episode {episode+1}/{episodes}")
    obs, _ = env.reset()
    done = False
    total_reward = 0

    while not done:
        print("Current State:", obs)
        action, _ = model.predict(
            obs,
            deterministic=True
        )

        obs, reward, done, _, _ = env.step(action)
        total_reward += reward
        print(f"Action: {action}, Reward: {reward}, Done: {done}")

    if total_reward > 0:
        success += 1

print(f"Success Rate: {success/episodes*100:.2f}%")