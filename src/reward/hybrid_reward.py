from src.reward.structured_reward import calculate_reward
from src.reward.llm_reward import calculate_llm_reward
from src.reward.adaptive_reward import AdaptiveReward

# created a hyperparameter to cosider the LLM influcne on rewards
# alpha_r ranges fro 0 to 1.
# 0 means no LLM influence on rewards
# 1 means consider full LLM rewards for total rewards calculation
# ALPHA_R = 0.2 (no longer used, now adaptive alpha is used based on RCA confidence)
reward_engine = AdaptiveReward()

def calculate_hybrid_reward(structured_reward, llm_score, confidence):
    # LLM given score converted to rewards
    llm_reward = (calculate_llm_reward(llm_score))

    reward, alpha = reward_engine.hybrid_reward(
        env_reward=structured_reward,
        llm_reward = llm_reward,
        confidence=confidence
    )

    return reward, alpha