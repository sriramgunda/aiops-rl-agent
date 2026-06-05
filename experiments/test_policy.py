from stable_baselines3 import PPO
from src.environment.aiops_env import AIOpsEnv
from src.environment.actions import ACTIONS
import numpy as np

env = AIOpsEnv()
model = PPO.load("results/ppo/ppo_model")
for incident in [
    "cpu_spike",
    "memory_leak",
    "service_crash",
    "db_latency",
    "dependency_failure"
]:
    state = env.generator.generate()
    state["incident"] = incident
    env.state = state
    obs = env._obs()
    action, _ = model.predict(obs,deterministic=True)
    if isinstance(action, np.ndarray):
        action = int(action.item())
    print(incident, " -> ", ACTIONS[action])