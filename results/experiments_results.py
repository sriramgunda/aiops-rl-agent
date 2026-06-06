# Phase 1 - DQN vs PPO Baseline Comparison
DQN_initial_metrics = {'avg_reward': 24.01, 'max_reward': 50, 'min_reward': -30,'action_accuracy': 0.605,
                       'action_distribution': {'restart_service': 481, 'clear_cache': 500, 'dependency_check': 19}}
PPO_initial_metrics = {'avg_reward': 29.89, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.663,
                       'action_distribution': {'restart_service': 703, 'clear_cache': 195, 'scale_up': 102}}

# Phase 2 - RCA-Augmented State Comparison
DQN_RCA_metrics = {'avg_reward': 33.7, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.788,
                   'action_distribution': {'restart_service': 421, 'clear_cache': 320, 'scale_up': 259}}
PPO_RCA_metrics = {'avg_reward': 22.925, 'max_reward': 50, 'min_reward': -10, 'action_accuracy': 0.527,
                   'action_distribution': {'restart_service': 828, 'scale_up': 123, 'clear_cache': 49}}