# Define the effects of actions on different types of incidents
# Each action has a specific impact on the incident,
# which can be positive (improvement) or negative (deterioration).
# This mapping is used to calculate the reward for the RL agent
# based on the action taken and the incident type
ACTION_EFFECTS = {
    "cpu_spike": {
        "scale_up": 50,
        "restart_service": -10,
        "rollback": -20,
        "clear_cache": -5,
        "dependency_check": -10,
        "no_action": -25
    },

    "memory_leak": {
        "restart_service": 50,
        "scale_up": -10,
        "rollback": -10,
        "clear_cache": -5,
        "dependency_check": -10,
        "no_action": -25
    },

    "service_crash": {
        "restart_service": 50,
        "rollback": 30,
        "scale_up": -10,
        "no_action": -30
    },

    "db_latency": {
        "clear_cache": 50,
        "restart_service": -5,
        "scale_up": -5,
        "no_action": -25
    },

    "dependency_failure": {
        "dependency_check": 50,
        "restart_service": -10,
        "no_action": -30
    }
}