# Evaluator class to assess the performance of the trained RL agent
from collections import Counter
import pandas as pd
import numpy as np

from src.environment.actions import ACTIONS
from src.utils.seeding import set_seed

#set_seed(42)

STEP_DURATION_MINUTES = 5 # Assumption of step duration for MTTR calculation

class Evaluator:
    def __init__(self, env, model):
        self.env = env
        self.model = model

    def evaluate(self, episodes=1000):
        total_rewards = []
        total_steps = []
        resolved_steps = []
        successful_actions = []
        success_count = 0
        avg_mttr = 0

        action_counter = Counter()
        incident_counts = Counter()
        total_actions = 0

        correct_actions = 0

        for _ in range(episodes):
            obs, _ = self.env.reset()
            done = False
            episode_reward = 0
            episode_steps = 0

            incident = self.env.state["incident"]
            incident_counts[incident] += 1

            while not done:
                action, _ = self.model.predict(
                    obs,
                    deterministic=True
                )

                if isinstance(action, np.ndarray):
                    action = int(action.item())

                action_name = ACTIONS[action]
                action_counter[action_name] += 1
                # expected = self.env.expert_action(incident)
                expected_idx = self.env.state["recommended_action"]
                expected = ACTIONS[expected_idx]

                if action_name == expected:
                    correct_actions += 1

                obs, reward, done, _, info = self.env.step(action)

                episode_reward += reward
                episode_steps += 1
            
            total_rewards.append(episode_reward)
            total_steps.append(episode_steps)

            if info.get("success", False):
                success_count += 1
                resolved_steps.append(episode_steps)
                successful_actions.append(action_name)
        
        if resolved_steps:
            avg_mttr = np.mean(resolved_steps) * STEP_DURATION_MINUTES
        
        for k, v in action_counter.items():
            total_actions += v
        
        # how many expert actions followed
        recommendation_follow_rate = round(correct_actions/total_actions, 4)
        
        # print(total_rewards)
        print(f"correct_actions: {correct_actions}")
        print(f"total_steps_sum: {sum(total_steps)}")
        print(f"success_count: {success_count}")
        # print(f"total_steps: {total_steps}")

        return {
            "episodes": episodes,
            "avg_reward": round(np.mean(total_rewards)),
            "max_reward": round(np.max(total_rewards)),
            "min_reward": round(np.min(total_rewards)),
            "recommendation_follow_rate": recommendation_follow_rate,
            "success_rate": round(success_count / episodes, 4),
            "avg_steps": round(np.mean(total_steps)),
            "max_steps": round(np.max(total_steps)),
            "mttr_minutes": round(float(avg_mttr) , 2),
            "action_distribution": dict(action_counter),
            "successful_action_distribution": dict(Counter(successful_actions)),
            "incident_types": dict(incident_counts),         
        }