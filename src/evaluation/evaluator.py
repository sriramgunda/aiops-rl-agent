# Evaluator class to assess the performance of the trained RL agent
from collections import Counter
import pandas as pd
import numpy as np

from src.environment.actions import ACTIONS

class Evaluator:
    def __init__(self, env, model):
        self.env = env
        self.model = model

    def evaluate(self, episodes=1000):
        rewards = []
        action_counter = Counter()

        correct_actions = 0

        for _ in range(episodes):
            obs, _ = self.env.reset()
            incident = self.env.state["incident"]
            action, _ = self.model.predict(
                obs,
                deterministic=True
            )

            if isinstance(action, np.ndarray):
                action = int(action.item())

            action_name = ACTIONS[action]
            action_counter[action_name] += 1
            expected = self.env.expert_action(incident)

            if action_name == expected:
                correct_actions += 1

            obs, reward, done, _, _ = self.env.step(action)
            rewards.append(reward)

        return {
            "avg_reward": sum(rewards)/len(rewards),
            "max_reward": max(rewards),
            "min_reward": min(rewards),
            "action_accuracy": correct_actions/episodes,
            "action_distribution": dict(action_counter)
        }