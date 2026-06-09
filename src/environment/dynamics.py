# Define the effects of actions on different types of incidents
# Each action has a specific impact on the incident,
# which can be positive (improvement) or negative (deterioration).
# This mapping is used to calculate the reward for the RL agent
# based on the action taken and the incident type
ACTION_EFFECTS = {
    "cpu_spike": {
        "scale_up": {
            "cpu": -35,
            "latency": -200,
            "error_rate": -10
        },
        "restart_service": {
            "cpu": -5,
            "latency": -50,
            "error_rate": -2
        },
        "clear_cache": {
            "latency": -40
        }
    },

    "memory_leak": {
        "restart_service": {
            "memory": -45,
            "latency": -150,
            "error_rate": -10,
            "pod_restart": -1
        },
        "scale_up": {
            "memory": -5,
            "latency": -10,
            "error_rate": -1,
        }
    },

    "service_crash": {
        "restart_service": {
            "error_rate": -50,
            "latency": -400,
            "http_500": -1,
            "pod_restart": -1
        },

        "rollback": {
            "error_rate": -40,
            "latency": -300,
            "http_500": -1
        }
    },

    "db_latency": {
        "clear_cache": {
            "latency": -700,
            "error_rate": -20,
            "db_timeout": -1
        },
        "scale_up": {
            "latency": -100,
            "error_rate": -10,
        }
    },

    "dependency_failure": {
        "dependency_check": {
            "error_rate": -30,
            "latency": -450,
            "upstream_timeout": -1
        },
        "scale_up": {
            "latency": -10,
            "error_rate": -1,
        }
    },

    "no_incident": {
        "no_action": {
            "cpu": 0,
            "latency": 0,
            "error_rate": 0
        }
    }
}