from src.environment.aiops_env import AIOpsEnv
from src.environment.actions import ACTIONS, ACTIONS_MAP_NUM

env = AIOpsEnv()

obs, _ = env.reset(seed=42)

print(f"Initial State: {env.state}")

done = False
total_reward = 0

print("\nEpisode Started")
action = env.action_space.sample()
while not done:        
    print(f"\nAction selected: {ACTIONS[action]}")
    obs, reward, done, _, info = env.step(action)
    #print("New State:", env.state)
    print("Reward:", reward)
    #print("Info:", info)

    total_reward += reward
    #action = env.state["recommended_action"]
    action = ACTIONS_MAP_NUM[info["next state"]['rag result']["recommended_action"]]

print("\nEpisode Finished")
print("Total Reward:", total_reward)