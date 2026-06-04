# This file defines the dynamics of the environment,
# including how actions affect the state and the reward structure.
ACTION_EFFECTS = {
    "cpu_spike":{
        "recommend_scale_up":{
            "cpu":-45,
            "latency":-120,
            "error_rate":-5,
            "reward":10
        },

        "recommend_restart_service":{
            "cpu":-10,
            "latency":-30,
            "reward":2
            },

        "recommend_clear_cache":{
            "latency":-40,
            "reward":1
            },

        "recommend_rollback":{
            "reward":-3
            },

        "recommend_dependency_check":{
            "reward":0
            }
    },

    "memory_leak":{
        "recommend_restart_service":{
            "memory":-50,
            "reward":10
            },

        "recommend_scale_up":{
            "memory":-5,
            "reward":1
            }
    },

    "service_crash":{
        "recommend_restart_service":{
            "error_rate":-70,
            "latency":-150,
            "reward":10
            },

        "recommend_rollback":{
            "error_rate":-40,
            "reward":6
            }
    },

    "db_latency":{
        "recommend_clear_cache":{
            "latency":-350,
            "reward":10
            }
    },

    "dependency_failure":{
        "recommend_dependency_check":{
            "error_rate":-50,
            "reward":10
            }
    }
}