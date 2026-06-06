# State builder for AIOps RL Agent

INCIDENT_MAP = {
    "cpu_spike":0,
    "memory_leak":1,
    "service_crash":2,
    "db_latency":3,
    "dependency_failure":4
}

def build_state(metrics, rca):
    # Combine metrics and RCA analysis into a single state representation
    return [
        metrics["cpu"],
        metrics["memory"],
        metrics["latency"],
        metrics["error_rate"],
        INCIDENT_MAP[rca["incident"]],
        rca["confidence"]
    ]