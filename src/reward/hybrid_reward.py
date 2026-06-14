from src.reward.structured_reward import calculate_reward
from src.reward.llm_reward import calculate_llm_reward

# created a hyperparameter to cosider the LLM influcne on rewards
# alpha_r ranges fro 0 to 1.
# 0 means no LLM influence on rewards
# 1 means consider full LLM rewards for total rewards calculation
ALPHA_R = 0.2

def calculate_hybrid_reward(structured_reward, llm_score, alpha=ALPHA_R):
    # LLM given score converted to rewards
    llm_reward = (calculate_llm_reward(llm_score))
    return (structured_reward + alpha * llm_reward)