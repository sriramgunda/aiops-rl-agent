# This file defines the reward structure for the AIOps agent.
def structured_reward(before, after, action_reward):
    '''Calculates the reward based on the change in system metrics and the action taken.
    The reward is a weighted sum of the improvements in CPU usage, latency, and error rate'''

    weights = {
        "cpu": 0.3,
        "latency": 0.4,
        "error_rate": 0.3
    }
    cpu_gain = before["cpu"] - after["cpu"]

    latency_gain = before["latency"] - after["latency"]

    error_gain = before["error_rate"]- after["error_rate"]

    reward = (
        weights["cpu"] * cpu_gain +
        weights["latency"] * latency_gain +
        weights["error_rate"] * error_gain +
        action_reward
    )

    return reward/100