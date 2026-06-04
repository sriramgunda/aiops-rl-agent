# This code is for testing the trained PPO model on the AIOps environment.
# It runs through a set of predefined incidents and checks the action
# chosen by the model for each incident.
from stable_baselines3 import PPO
from environment.rl_env import AIOpsEnv
from environment.actions import ACTIONS

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

model = PPO.load("models/ppo_aiops")

env = AIOpsEnv()

for incident in [
    "cpu_spike",
    "memory_leak",
    "service_crash",
    "db_latency",
    "dependency_failure"]:

    env.current_incident = incident
    env.state = env.simulator_state(incident)
    obs = env._obs()
    action, _ = model.predict(
        obs,
        deterministic=True
    )

    print(incident, "->", ACTIONS[action])