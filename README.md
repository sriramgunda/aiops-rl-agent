
## Experiments and Results at each phase
### Phase 1 - Train DQN and PPO only
- **Architecture**: metrics -> RL agent (DQN/PPO)
- **Workflow**: incident -> action -> reward -> Done
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
- **DQN results**: 
  {'avg_reward': 24.01, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.605, 'action_distribution': {'restart_service': 481, 'clear_cache': 500, 'dependency_check': 19}}
- **PPO results**:
{'avg_reward': 29.89, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.663, 'action_distribution': {'restart_service': 703, 'clear_cache': 195, 'scale_up': 102}}

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
- **DQN results**: 
  {'avg_reward': 33.7, 'max_reward': 50, 'min_reward': -30, 'action_accuracy': 0.788, 'action_distribution': {'restart_service': 421, 'clear_cache': 320, 'scale_up': 259}}
- **PPO results**:
{'avg_reward': 22.925, 'max_reward': 50, 'min_reward': -10, 'action_accuracy': 0.527, 'action_distribution': {'restart_service': 828, 'scale_up': 123, 'clear_cache': 49}}


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


### Phase 3 - Train DQN and PPO with multi-step remediation
#### Added multi-step MDP remediation and observability signals for RL agents to learn
- **Architecture**: metrics -> RAG -> RCA -> incident class, confidence -> RL agent (DQN/PPO)
- **Workflow**: incident -> action 1 -> update metrics -> action 2 -> update metrics -> action 3 -> Resolved
- Incident will be marked as resolved if latency < 300ms and error_rate < 5 or max_steps = 5
- Implemented structured reward function using metrics.
- Updated metrics clamping to avoid negative values.
- MTTR metric is introduced for baseline comparison along with other metrics
- Assumption made for step time duration as 5min to calculate MTTR. That means, if agent takes 3 steps to complete then MTTR will be 3 * 5 = 15min.
- Considering the simulated AIOps environment, Mean Time To Resolve (MTTR) is approximated using the number of remediation actions required to successfully resolve an incident. Each remediation step is assumed to represent a fixed operational interval of five minutes. Therefore, MTTR is calculated as:
MTTR = Average Successful Resolution Steps × 5 minutes
This approximation enables quantitative comparison of remediation efficiency across DQN, PPO, and LLM-guided reinforcement learning agents while maintaining consistency across experimental conditions.
- **MDP Formulation**:
	- State -> Action -> New State -> Action -> New State -> ... -> Resolution
	- ***State Space***
		- S = [cpu, memory, latency, error_rate, http_500, db_timeout, upstream_timeout, pod_restart, incident_class, confidence, recommended_action]
		- S dimension = 11
	- ***Action Space***
		- A = {0: restart_service, 1: scale_up, 2: clear_cache, 3: rollback, 4: dependency_check, 5: no_action}
		- A dimension = 6
	- ***Transition Function***
		- s(t+1)=T(s(t), a(t))
		- metrics will change after every action
	- ***Reward Function***
		- R(s,a) = (latency improvement + error reduction + cpu recovery - step penalty)
	- ***Policy***
		- DQN - π_DQN(a|s)
		- PPO - π_PPO(a|s)
	- ***Termination***
		- resolved or max steps reached
- **DQN results**: 
 {'episodes': 1000, 'avg_reward': 44, 'max_reward': 431, 'min_reward': -20, 'recommendation_follow_rate': 0.0, 'success_rate': 0.154, 'avg_steps': 5, 'max_steps': 5, 'mttr_minutes': 11.27, 'action_distribution': {'rollback': 4383, 'scale_up': 40, 'clear_cache': 154}, 'successful_action_distribution': {'rollback': 153, 'scale_up': 1}, 'incident_types': {'db_latency': 206, 'dependency_failure': 199, 'service_crash': 202, 'memory_leak': 196, 'cpu_spike': 197}}
- **PPO results**:
{'episodes': 1000, 'avg_reward': 185, 'max_reward': 548, 'min_reward': -20, 'recommendation_follow_rate': 0.3415, 'success_rate': 0.564, 'avg_steps': 3, 'max_steps': 5, 'mttr_minutes': 8.69, 'action_distribution': {'dependency_check': 908, 'scale_up': 845, 'clear_cache': 229, 'restart_service': 1178}, 'successful_action_distribution': {'scale_up': 251, 'restart_service': 253, 'clear_cache': 33, 'dependency_check': 27}, 'incident_types': {'service_crash': 219, 'cpu_spike': 191, 'db_latency': 190, 'memory_leak': 214, 'dependency_failure': 186}}

#### Comparison
|Metric|DQN|PPO
|--|--|--
| Avg Reward | 44 |185
| Success Rate| 15.4% |56.4%
| MTTR | 11.27 min |8.69 min
| Avg Steps | 5 |3
| Recommendation Follow Rate | 0% |34.1%

#### Observations
- PPO is clearly outperforming DQN in all key metrics
- This proves that PPO is better suited than DQN for sequential incident remediation tasks in an autonomous AIOps environment.
- PPO learned incident-specific policies efficiently
- The Recommendation Follow Rate metric is a hint for RL agent to take recommended action. PPO utilizing the hint and exploring in other times.
- MTTR metric highlights that PPO is resolving the incident in less time.
- PPO now improved and performed better with multi-step environment, RCA and recommended hints, structured rewards.
- However constructing structured rewards took lot of time to optimize the function. The metrics and signals are tricky and they need proper weights for RL agents to learn efficiently.
- There could be hidden state dimensions and dynamics and hard to include all scenarios of issues in the environment.
- For instance, though the environment is healthy, error rate could be high due to unexpected errors like client network latency, external factors etc. or the actions taken are not fully resolved the incident in given time. All these metrics are hard to capture and identify proactively.
- This is where LLM can help to provide efficient dynamics and reasons for RL agent on the incident resolution steps it has taken. 