
## Experiments and Results at each phase
### Phase 1 - Train DQN and PPO only
- **Architecture**: metrics -> RL agent (DQN/PPO)
- **Workflow**: incident -> action -> reward -> Done
- **DQN results**: 
  {'avg_reward': 24.01, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.605, 'action_distribution': {'restart_service': 481, 'clear_cache': 500, 'dependency_check': 19}}
- **PPO results**:
{'avg_reward': 29.89, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.663, 'action_distribution': {'restart_service': 703, 'clear_cache': 195, 'scale_up': 102}}
- **MDP Formulation**:
	- ***State Space***
		- S = [cpu, memory, latency, error_rate ]
		- S dimension = 4
	- ***Action Space***
		- A = {0: restart_service, 1: scale_up, 2: clear_cache, 3: rollback, 4: dependency_check, 5: no_action}
		- A dimension = 6
	- ***Transition Function***
		- P(s`|s,a): State -> One Action -> Reward -> Terminal State
	- ***Reward Function***
		- R(s,a) = action_effects[incident][action]
	- ***Policy***
		- DQN - π_DQN(a|s)
		- PPO - π_PPO(a|s)


#### Comparison
|Metric|DQN|PPO
|--|--|--
| Average reward | 24.01 |29.89
| Accuracy | 60.5% |66.3%
| Max Reward | 50 |50
| Min Reward | -30 |-30

#### Observations
- PPO performed better than DQN
- But both algorithms have problem with action distribution
- ***Policy collapse***
	- DQN
		- restart_service : 481
clear_cache     : 500
dependency_check: 19
scale_up        : 0
rollback        : 0
	- PPO
		- restart_service : 703
clear_cache     : 195
scale_up        : 102
dependency_check : 0
rollback         : 0
- Neither agent learned the recommended actions properly
- When some actions gives more rewards, agents tried those actions repeatedly
- This is because the current state only has metrics [cpu, memory, latency, error_rate] and agents didnt seen the incident_type. The state representation didnt included the incident label.
- For instance, here are sample metrics [90,60,250,10] and agent is trying to infer incident class from noisy metrics.
- Also, the environment is configured to stop after single action that means agents not learning the sequential remediation. This is set for one step environment intentionally to see the results of DQN and PPO by providing minimal details about state and environment,

#### Plot Comparison
- DQN vs PPO Accuracy comparison
![DQN vs PPO Accuracy comparison](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/accuracy_comparison_initial.png)

- Reward comparison
![Reward comparison](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/reward_comparison_initial.png)

- Action comparison
![Action comparison](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/action_comparison_initial.png)

- DQN Action distribution
![DQN Actions](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/dqn_action_distribution_initial.png)

- PPO Action distribution
![PPO Actions](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/ppo_action_distribution_initial.png)


### Phase 2 - Train DQN and PPO with RAG and RCA
#### Integrated RCA and RAG
- **Architecture**: metrics -> RAG -> RCA -> incident class, confidence -> RL agent (DQN/PPO)
- **Workflow**: incident -> action -> reward -> Done
- The state has additional information metrics + incident class + confidence
- The state now becomes [cpu, memory, latency, error_rate, incident_id, confidence]
- Added historical incidents, RAG retriever, RCA (without LLM, extract rca details from past incidents labels and metadata), state_builder (included incident type and confidence), integrated RAG and RCA into AIOps environment
- **DQN results**: 
  {'avg_reward': 33.7, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.788, 'action_distribution': {'restart_service': 421, 'clear_cache': 320, 'scale_up': 259}}
- **PPO results**:
{'avg_reward': 22.925, 'max_reward': 50, 'min_reward': -10, 'action_accuracy': 0.527, 'action_distribution': {'restart_service': 828, 'scale_up': 123, 'clear_cache': 49}}
- **MDP Formulation**:
	- ***State Space***
		- S = [cpu, memory, latency, error_rate, incident_class, confidence]
		- S dimension = 6
	- ***Action Space***
		- A = {0: restart_service, 1: scale_up, 2: clear_cache, 3: rollback, 4: dependency_check, 5: no_action}
		- A dimension = 6
	- ***Transition Function***
		- P(s`|s,a): State -> One Action -> Reward -> Terminal State
	- ***Reward Function***
		- R(s,a) = action_effects[incident][action]
	- ***Policy***
		- DQN - π_DQN(a|s)
		- PPO - π_PPO(a|s)

#### Comparison
|Model|Average reward|Accuracy 
|--|--|--
| DQN baseline | 24.01 |60.5%
| PPO baseline| 29.89 |66.3%
| DQN + RCA | 33.7 |78.8%
| PPO + RCA | 22.925 |52.7%

#### Observations
- DQN performed better than PPO
- DQN improved better with RCA integration but PPO got worse scores because PPO is not using the new state representation properly.
- PPO policy collapse still exists. PPO has learned that restart_service policy is usually safe and keeps exploiting it.
- DQN performed well here because, there is no sequential action decisions. Environment has single step decision and discrete actions, so DQN eventually improved better with more information.
- In a single-step incident remediation recommendation environment, DQN outperformed PPO after incorporating RCA-derived state information.

#### Plot Comparison
- DQN vs PPO Accuracy comparison
![DQN vs PPO Accuracy comparison](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/accuracy_comparison_after_rca.png)

- Reward comparison
![Reward comparison](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/reward_comparison_after_rca.png)

- Action comparison
![Action comparison](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/action_comparison_rca.png)

- DQN Action distribution
![DQN Actions](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/dqn_action_distribution_rca.png)

- PPO Action distribution
![PPO Actions](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/ppo_action_distribution_rca.png)

- Impact of adding RCA
![RCA Impact](https://raw.githubusercontent.com/sriramgunda/aiops-rl-agent/refs/heads/feature/v1/results/plots/rca_impact.png)

