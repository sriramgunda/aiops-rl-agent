# Expert policy mapping specific incidents to their corresponding actions
EXPERT_POLICY = {
    "cpu_spike": "scale_up",
    "memory_leak": "restart_service",
    "service_crash": "restart_service",
    "db_latency": "clear_cache",
    "dependency_failure": "dependency_check"
}