import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Ensure project root is on sys.path so top-level packages like `results` can be imported
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from results.experiments_results import DQN_initial_metrics, PPO_initial_metrics, DQN_RCA_metrics, PPO_RCA_metrics
PLOTS_DIR = Path("results/plots")

PLOTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Define the metrics for each model based on the evaluation results.
metrics = pd.DataFrame({
    "Model": [
        "DQN",
        "PPO",
        "DQN + RCA",
        "PPO + RCA"
    ],

    "AvgReward":[
        DQN_initial_metrics['avg_reward'],
        PPO_initial_metrics['avg_reward'],
        DQN_RCA_metrics['avg_reward'],
        PPO_RCA_metrics['avg_reward']
    ],

    "Accuracy":[
        DQN_initial_metrics['action_accuracy'] * 100,
        PPO_initial_metrics['action_accuracy'] * 100,
        DQN_RCA_metrics['action_accuracy'] * 100,
        PPO_RCA_metrics['action_accuracy'] * 100
    ],

    "ActionDistribution":[
        DQN_initial_metrics['action_distribution'],
        PPO_initial_metrics['action_distribution'],
        DQN_RCA_metrics['action_distribution'],
        PPO_RCA_metrics['action_distribution']
    ]
})

# Plotting the metrics
# ==================================
# Accuracy comparison plot
# ==================================

# Phase 1 - DQN vs PPO accuracy comparison
plt.figure(figsize=(10,5))
plt.bar(
    metrics["Model"][0:2],
    metrics["Accuracy"][0:2]
)
plt.ylabel("Accuracy (%)")
plt.title("DQN vs PPO Accuracy")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "accuracy_comparison_initial.png")
plt.show()

# Phase 2 - DQN vs PPO accuracy comparison after RCA augmentation
plt.figure(figsize=(10,5))
plt.bar(
    metrics["Model"],
    metrics["Accuracy"]
)
plt.ylabel("Accuracy (%)")
plt.title("DQN vs PPO Accuracy")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "accuracy_comparison_after_rca.png")
plt.show()

# ==================================
# Average reward comparison plot
# ==================================
# Phase 1 - DQN vs PPO average reward comparison
plt.figure(figsize=(10,5))
plt.bar(
    metrics["Model"][0:2],
    metrics["AvgReward"][0:2])
plt.ylabel("Average Reward")
plt.title("DQN vs PPO Average Reward")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "reward_comparison_initial.png")
plt.show()

# Phase 2 - DQN vs PPO average reward comparison after RCA augmentation
plt.figure(figsize=(10,5))
plt.bar(
    metrics["Model"],
    metrics["AvgReward"])
plt.ylabel("Average Reward")
plt.title("DQN vs PPO Average Reward")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "reward_comparison_after_rca.png")
plt.show()

# =================================
# Baseline vs RCA comparison plot
# =================================
improvement = pd.DataFrame({
    "Model":["DQN", "PPO"],
    "Initial":[DQN_initial_metrics['action_accuracy'] * 100, PPO_initial_metrics['action_accuracy'] * 100],
    "RCA":[DQN_RCA_metrics['action_accuracy'] * 100, PPO_RCA_metrics['action_accuracy'] * 100]
})
plt.figure(figsize=(8,5))
x = range(len(improvement))
plt.bar(
    x,
    improvement["Initial"],
    width=0.4,
    label="Initial"
)
plt.bar(
    [i+0.4 for i in x],
    improvement["RCA"],
    width=0.4,
    label="RCA"
)
plt.xticks(
    [i+0.2 for i in x],
    improvement["Model"]
)
plt.ylabel("Accuracy (%)")
plt.legend()
plt.title("Impact of RCA-Augmented State")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "rca_impact.png")
plt.show()

# =================================
# Action distribution plot
# =================================
# Phase 1 - DQN action distribution
dqn_actions = {k: v for k, v in DQN_initial_metrics['action_distribution'].items() if v > 0}
plt.figure(figsize=(8,6))
plt.pie(
    dqn_actions.values(),
    labels=dqn_actions.keys(),
    autopct="%1.1f%%"
)
plt.title("DQN Action Distribution")
plt.savefig(PLOTS_DIR / "dqn_action_distribution_initial.png")
plt.show()

# PPO action distribution
ppo_actions = {k: v for k, v in PPO_initial_metrics['action_distribution'].items() if v > 0}
plt.figure(figsize=(8,6))
plt.pie(
    ppo_actions.values(),
    labels=ppo_actions.keys(),
    autopct="%1.1f%%"
)
plt.title("PPO Action Distribution")
plt.savefig(PLOTS_DIR / "ppo_action_distribution_initial.png")
plt.show()

# Phase 2 - DQN action distribution after RCA augmentation
dqn_rca_actions = {k: v for k, v in DQN_RCA_metrics['action_distribution'].items() if v > 0}
plt.figure(figsize=(8,6))
plt.pie(
    dqn_rca_actions.values(),
    labels=dqn_rca_actions.keys(),
    autopct="%1.1f%%"
)
plt.title("DQN Action Distribution (RCA)")
plt.savefig(PLOTS_DIR / "dqn_action_distribution_rca.png")
plt.show()

# PPO action distribution after RCA augmentation
ppo_rca_actions = {k: v for k, v in PPO_RCA_metrics['action_distribution'].items() if v > 0}
plt.figure(figsize=(8,6))
plt.pie(
    ppo_rca_actions.values(),
    labels=ppo_rca_actions.keys(),
    autopct="%1.1f%%"
)
plt.title("PPO Action Distribution (RCA)")
plt.savefig(PLOTS_DIR / "ppo_action_distribution_rca.png")
plt.show()


# =================================
# DQN vs PPO action distribution comparison
# =================================
all_actions = [
        "no_action",
        "scale_up",
        "clear_cache",
        "rollback",
        "dependency_check",
        "restart_service"
    ]
# Phase 1 - DQN vs PPO action distribution comparison
action_df = pd.DataFrame({
    "Action": all_actions,
    "DQN": [DQN_initial_metrics['action_distribution'].get(action, 0) for action in all_actions],
    "PPO": [PPO_initial_metrics['action_distribution'].get(action, 0) for action in all_actions]
})

action_df.set_index("Action").plot(kind="bar",figsize=(10,5))
plt.ylabel("Count")
plt.title("Action Selection Comparison")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "action_comparison_initial.png")
plt.show()

# Phase 2 - DQN vs PPO action distribution comparison after RCA augmentation
action_df_rca = pd.DataFrame({
    "Action": all_actions,
    "DQN RCA": [DQN_RCA_metrics['action_distribution'].get(action, 0) for action in all_actions],
    "PPO RCA": [PPO_RCA_metrics['action_distribution'].get(action, 0) for action in all_actions]
})
action_df_rca.set_index("Action").plot(kind="bar",figsize=(10,5))
plt.ylabel("Count")
plt.title("Action Selection Comparison (RCA)")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "action_comparison_rca.png")
plt.show()

# Accuracy comparison across all models
comparison = pd.DataFrame({
    "Model":[
        "DQN",
        "PPO",
        "DQN RCA",
        "PPO RCA"
    ],

    "Accuracy":[
        DQN_initial_metrics['action_accuracy'] * 100,
        PPO_initial_metrics['action_accuracy'] * 100,
        DQN_RCA_metrics['action_accuracy'] * 100,
        PPO_RCA_metrics['action_accuracy'] * 100
    ]
})

plt.figure(figsize=(10,6))
bars = plt.bar(
    comparison["Model"],
    comparison["Accuracy"]
)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{bar.get_height():.1f}%",
        ha="center"
    )

plt.ylabel("Accuracy (%)")
plt.title("Accuracy Comparison Across Models")
plt.tight_layout()
plt.savefig(PLOTS_DIR / "final_accuracy_comparison.png")
plt.show()
