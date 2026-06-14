# Convert LLM score (0 to 100) to rewards
# Since LLM produces probablity scores,
# the prompt will enforce LLM to provide score in the speficied range.
# This helps to calculate the influence of LLM on rewards.

def calculate_llm_reward(llm_score):
    return (llm_score - 50) / 10.0