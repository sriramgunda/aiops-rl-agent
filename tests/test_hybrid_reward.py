from src.reward.hybrid_reward import calculate_hybrid_reward

structured = 100
for score in [
    100,
    80,
    50,
    20,
    0
]:

    total = calculate_hybrid_reward(
        structured_reward=structured,
        llm_score=score,
        alpha=0.9
    )

    print(f"LLM Score = {score} - Total Score = {total}")