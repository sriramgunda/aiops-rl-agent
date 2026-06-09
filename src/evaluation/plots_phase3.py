import os
import matplotlib.pyplot as plt

os.makedirs("results/plots", exist_ok=True)
# -----------------------------
# Latest Results
# -----------------------------
dqn = {
    "avg_reward": 44,
    "success_rate": 15.4,
    "mttr": 11.27,
    "avg_steps": 5,
    "follow_rate": 0.0
}
ppo = {
    "avg_reward": 185,
    "success_rate": 56.4,
    "mttr": 8.69,
    "avg_steps": 3,
    "follow_rate": 34.15
}
dqn_actions = {
    "rollback": 4383,
    "scale_up": 40,
    "clear_cache": 154
}
ppo_actions = {
    "dependency_check": 908,
    "scale_up": 845,
    "clear_cache": 229,
    "restart_service": 1178
}
dqn_incident_distribution = {
    "cpu_spike":197,
    "memory_leak":196,
    "service_crash":202,
    "db_latency":206,
    "dependency_failure":199
}
ppo_incident_distribution = {
    "cpu_spike":191,
    "memory_leak":214,
    "service_crash":219,
    "db_latency":190,
    "dependency_failure":186
}


algorithms = ["DQN", "PPO"]

# ===================================================
# 1. Average Reward
# ===================================================
plt.figure(figsize=(8,5))
plt.bar(algorithms, [dqn["avg_reward"], ppo["avg_reward"]])

plt.title("Average Reward Comparison")
plt.ylabel("Average Reward")
plt.tight_layout()
plt.savefig("results/plots/avg_reward_comparison.png")
plt.close()

# ===================================================
# 2. Success Rate
# ===================================================
plt.figure(figsize=(8,5))
plt.bar(algorithms, [dqn["success_rate"], ppo["success_rate"]])
plt.title("Success Rate Comparison")
plt.ylabel("Success Rate (%)")
plt.tight_layout()
plt.savefig("results/plots/success_rate_comparison.png")
plt.close()

# ===================================================
# 3. MTTR
# ===================================================
plt.figure(figsize=(8,5))
plt.bar(algorithms, [dqn["mttr"], ppo["mttr"]])
plt.title("MTTR Comparison")
plt.ylabel("Minutes")
plt.tight_layout()
plt.savefig("results/plots/mttr_comparison.png")
plt.close()

# ===================================================
# 4. Average Steps
# ===================================================
plt.figure(figsize=(8,5))
plt.bar(algorithms, [dqn["avg_steps"], ppo["avg_steps"]])
plt.title("Average Steps to Resolution")
plt.ylabel("Steps")
plt.tight_layout()
plt.savefig("results/plots/avg_steps_comparison.png")
plt.close()

# ===================================================
# 5. Recommendation Follow Rate
# ===================================================
plt.figure(figsize=(8,5))
plt.bar(algorithms, [dqn["follow_rate"], ppo["follow_rate"]])
plt.title("Recommendation Follow Rate")
plt.ylabel("Percentage (%)")
plt.tight_layout()
plt.savefig("results/plots/recommendation_follow_rate.png")
plt.close()
print("Plots generated successfully.")

# ===================================================
# 6. Action Distribution
# ===================================================
# DQN
plt.figure(figsize=(8,5))
plt.bar(dqn_actions.keys(), dqn_actions.values())
plt.title("DQN Action Distribution")
plt.tight_layout()
plt.savefig("results/plots/dqn_action_distribution.png")
plt.close()

# PPO
plt.figure(figsize=(8,5))
plt.bar(ppo_actions.keys(), ppo_actions.values())
plt.title("PPO Action Distribution")
plt.tight_layout()
plt.savefig("results/plots/ppo_action_distribution.png")
plt.close()

# ===================================================
# 7. Incident Distribution
# ===================================================
# DQN
plt.figure(figsize=(10,5))
plt.bar(dqn_incident_distribution.keys(), dqn_incident_distribution.values())
plt.title("DQN Incident Distribution")
plt.tight_layout()
plt.savefig("results/plots/dqn_incident_distribution.png")
plt.close()

# PPO
plt.figure(figsize=(10,5))
plt.bar(ppo_incident_distribution.keys(), ppo_incident_distribution.values())
plt.title("PPO Incident Distribution")
plt.tight_layout()
plt.savefig("results/plots/ppo_incident_distribution.png")
plt.close()