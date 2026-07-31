# Performance Analysis

## Computational Performance

| Component               |   Average(ms) |   Percentage |
|:------------------------|--------------:|-------------:|
| Telemetry               |         0.012 |         0    |
| RAG                     |        16.269 |         1.12 |
| RCA                     |         0.009 |         0    |
| State Builder           |         0.086 |         0.01 |
| PPO                     |         1.564 |         0.11 |
| Environment Processing  |      1430.59  |        98.76 |
| Decision Pipeline Total |      1448.53  |       100    |

Average Decision Pipeline Latency: 1448.53 ms

## Scalability
- Decision Pipeline (ms): 1448.528
- Episode Latency (ms): 4706.231
- Episodes/sec: 0.212
- Incidents/hour: 763.2
- Incidents/day: 18316.8
- CPU (%): 61.885
- Memory (MB): 71.355

## Operational Performance
- Episodes: 1000
- Success Rate: 0.54
- Average Reward: 182
- Recommendation Follow Rate: 0.3464
- MTTR: 8.51
- Average Steps: 3

## Resource Usage
- CPU: 61.88%
- Memory: 71.36 MB