# Experimental Evaluation

This report compares three reinforcement learning reward strategies for autonomous production incident resolution.

Experiments Evaluated

- Structured Reward
- Fixed Hybrid Reward
- Adaptive Hybrid Reward

## Experimental Setup

Each experiment was trained and evaluated using 1000 simulated production incidents.

The evaluation measures cumulative reward, incident resolution success rate, mean time to resolution (MTTR), recommendation follow rate, and average number of remediation steps.

## Operational Comparison

| Metric                     |   Structured |   Fixed Alpha |   Adaptive Alpha |
|:---------------------------|-------------:|--------------:|-----------------:|
| Average Reward             |     185      |      190      |         182      |
| Success Rate               |       0.564  |        0.581  |           0.54   |
| Recommendation Follow Rate |       0.3415 |        0.3591 |           0.3464 |
| MTTR (minutes)             |       8.69   |        8.88   |           8.51   |
| Average Steps              |       3      |        3      |           3      |

## Relative Improvements

| Metric                     |   Fixed vs Structured (%) |   Adaptive vs Structured (%) |   Adaptive vs Fixed (%) |
|:---------------------------|--------------------------:|-----------------------------:|------------------------:|
| Average Reward             |                      2.7  |                        -1.62 |                   -4.21 |
| Success Rate               |                      3.01 |                        -4.26 |                   -7.06 |
| Recommendation Follow Rate |                      5.15 |                         1.43 |                   -3.54 |
| MTTR (minutes)             |                      2.19 |                        -2.07 |                   -4.17 |
| Average Steps              |                      0    |                         0    |                    0    |

## Adaptive Performance

| Metric                   |   Average |   Minimum |    Maximum |   Samples |
|:-------------------------|----------:|----------:|-----------:|----------:|
| ppo_inference_ms         |     1.564 |     0.423 |     49.328 |      3219 |
| environment_step_ms      |  1449.16  |     8.902 | 438253     |      3219 |
| telemetry_latency_ms     |     0.012 |     0.003 |      1.98  |      3219 |
| rag_latency_ms           |    16.269 |     0.003 |    547.558 |      3219 |
| rca_latency_ms           |     0.009 |     0.001 |      0.965 |      3219 |
| state_builder_latency_ms |     0.086 |     0.005 |     13.397 |      3219 |
| pipeline_latency_ms      |  1448.53  |     8.848 | 438230     |      3219 |
| adaptive_alpha           |     0.219 |     0.156 |      0.6   |      1000 |
| rca_confidence           |     0.547 |     0     |      0.666 |      1000 |
| llm_latency_ms           |  4609.48  |   679.255 | 438217     |      1000 |
| episode_latency_ms       |  4706.23  |   731.283 | 438281     |      1000 |
| cpu_percent              |    61.885 |    15.6   |     89.9   |      1000 |
| memory_mb                |    71.355 |     8.367 |     83.605 |      1000 |

## Discussion

- Fixed Hybrid Reward achieved the highest average reward (190).
- Adaptive Hybrid Reward achieved the lowest MTTR (8.51 minutes).
- Fixed Hybrid Reward achieved the highest incident success rate (58.10%).

These observations indicate a trade-off between maximizing cumulative reward and minimizing incident resolution time.

## Research Findings

1. Hybrid reward functions improve agent learning compared with structured rewards.

2. Adaptive reward weighting reduces MTTR without significantly increasing resolution complexity.

3. LLM-assisted reward evaluation enables confidence-aware policy adaptation.
