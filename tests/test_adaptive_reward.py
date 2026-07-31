from src.reward.hybrid_reward import calculate_hybrid_reward

structured_reward = 25
llm_score = 80

confidences = [0.95, 0.80, 0.60, 0.40, 0.20]

print("-" * 70)
print(f"{'Confidence':<15}{'Alpha':<15}{'Hybrid Reward'}")
print("-" * 70)

for confidence in confidences:

    reward, alpha = calculate_hybrid_reward(
        structured_reward=structured_reward,
        llm_score=llm_score,
        confidence=confidence
    )

    print(f"{confidence:<15.2f}{alpha:<15.3f}{reward:.3f}")