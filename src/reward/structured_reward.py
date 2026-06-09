# Structured Reward Function for AIOps RL Agent

# weights for different metrics in the reward calculation
weight_latency = 0.4
weight_error = 0.4
weight_cpu = 0.2

def calculate_reward(before, after, step_count):
    latency_gain = (before["latency"] - after["latency"])
    error_gain = (before["error_rate"] - after["error_rate"])
    cpu_gain = (before["cpu"] - after["cpu"])
    reward = (weight_latency * latency_gain + weight_error * error_gain + weight_cpu * cpu_gain)

    reward -= 1 * step_count  # Step penalty to encourage faster resolution
    return reward