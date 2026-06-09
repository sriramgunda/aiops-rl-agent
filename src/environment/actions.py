# The possible actions that the AIOps RL agent can take in the environment.
# Each action is represented by an integer key and a string value that describes the action.
ACTIONS = {
    0: "no_action",
    1: "scale_up",
    2: "clear_cache",
    3: "rollback",
    4: "dependency_check",
    5: "restart_service"
}

ACTIONS_MAP_NUM = {
    "no_action": 0,
    "scale_up": 1,
    "clear_cache": 2,
    "rollback": 3,
    "dependency_check": 4,
    "restart_service": 5
}