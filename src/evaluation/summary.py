import os
import matplotlib.pyplot as plt

# ==================================================
# Create output directory
# ==================================================
os.makedirs(
    "results/plots",
    exist_ok=True
)
# ==================================================
# Latest Evaluation Results
# ==================================================
dqn = {
    "success_rate": 15.4,
    "avg_reward": 44,
    "mttr": 11.27,
    "follow_rate": 0.0
}
ppo = {
    "success_rate": 56.4,
    "avg_reward": 185,
    "mttr": 8.69,
    "follow_rate": 34.15
}
algorithms = ["DQN", "PPO"]

# ==================================================
# Create 2x2 Summary Figure
# ==================================================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(
    "Autonomous AIOps Agent: DQN vs PPO Performance Comparison",
    fontsize=16,
    fontweight="bold"
)

# ==================================================
# 1. Success Rate
# ==================================================
axs[0, 0].bar(algorithms, [dqn["success_rate"], ppo["success_rate"]])
axs[0, 0].set_title("Success Rate (%)")
axs[0, 0].set_ylabel("Percentage")
for i, value in enumerate([dqn["success_rate"], ppo["success_rate"]]):
    axs[0, 0].text(
        i,
        value + 1,
        f"{value:.1f}%",
        ha="center"
    )

# ==================================================
# 2. Average Reward
# ==================================================
axs[0, 1].bar(algorithms, [dqn["avg_reward"], ppo["avg_reward"]])
axs[0, 1].set_title("Average Reward")
axs[0, 1].set_ylabel("Reward")
for i, value in enumerate([dqn["avg_reward"], ppo["avg_reward"]]):
    axs[0, 1].text(
        i,
        value + 5,
        str(value),
        ha="center"
    )

# ==================================================
# 3. MTTR
# ==================================================
axs[1, 0].bar(algorithms,[dqn["mttr"],ppo["mttr"]])
axs[1, 0].set_title("Mean Time To Resolution (MTTR)")
axs[1, 0].set_ylabel("Minutes")
for i, value in enumerate([dqn["mttr"],ppo["mttr"]]):
    axs[1, 0].text(
        i,
        value + 0.2,
        f"{value:.2f}",
        ha="center"
    )

# ==================================================
# 4. Recommendation Follow Rate
# ==================================================
axs[1, 1].bar(algorithms, [dqn["follow_rate"], ppo["follow_rate"]])
axs[1, 1].set_title("Recommendation Follow Rate (%)")
axs[1, 1].set_ylabel("Percentage")
for i, value in enumerate([dqn["follow_rate"], ppo["follow_rate"]]):
    axs[1, 1].text(
        i,
        value + 1,
        f"{value:.1f}%",
        ha="center"
    )

# ==================================================
# Layout
# ==================================================
plt.tight_layout()
plt.subplots_adjust(top=0.90)

# ==================================================
# Save
# ==================================================
output_file = ("results/plots/phase3_summary.png")
plt.savefig(
    output_file,
    dpi=300,
    bbox_inches="tight"
)
plt.close()
print(f"Summary plot saved: {output_file}")