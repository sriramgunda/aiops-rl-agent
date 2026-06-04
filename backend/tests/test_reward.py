# This is a simple test script to verify the functionality of the hybrid reward function.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from reward_engine.hybrid_reward import hybrid_reward

# a sample incident, action, and system states before and after the action
before = {"cpu":95, "latency":250, "error_rate":20}
after = {"cpu":45, "latency":110, "error_rate":5}

print(f"Reward: {hybrid_reward('cpu_spike', 'recommend_scale_up', before, after, 10)}")
#print(f"Overall reward: {hybrid_reward('cpu_spike', 'recommend_scale_up', before, after, 10)['overall']}")
