# Performance Analysis

## Throughput
- Episodes/sec: 0.26
- Incidents/hour: 936.0
- Incidents/day: 22464.0

## Component Contribution

| Component                |   Average(ms) |   Percentage |
|:-------------------------|--------------:|-------------:|
| telemetry_latency_ms     |         0.011 |         0    |
| rag_latency_ms           |        14.345 |         1.18 |
| rca_latency_ms           |         0.008 |         0    |
| state_builder_latency_ms |         0.04  |         0    |
| llm_latency_ms           |      3678.61  |       302.62 |

## Resource Usage
- CPU: 61.66%
- Memory: 72.36 MB