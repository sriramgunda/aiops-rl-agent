# State builder for AIOps RL Agent
from src.environment.actions import ACTIONS_MAP_NUM

INCIDENT_MAP = {
    "cpu_spike":0,
    "memory_leak":1,
    "service_crash":2,
    "db_latency":3,
    "dependency_failure":4,
    "no_incident":5
}

def build_state(metrics, rca):
    # Combine metrics and RCA analysis into a single state representation
    return [
        metrics["cpu"],
        metrics["memory"],
        metrics["latency"],
        metrics["error_rate"],
        metrics["http_500"],
        metrics["db_timeout"],
        metrics["upstream_timeout"],
        metrics["pod_restart"],
        INCIDENT_MAP[rca["incident"]],
        rca["confidence"],
        #ACTIONS_MAP_NUM[rca["recommended_action"]]
        metrics["recommended_action"]
    ]