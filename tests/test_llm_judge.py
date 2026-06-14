from src.llm.reward_judge import RewardJudge

judge = RewardJudge()

good_trajectory = {
    "incident": "cpu_spike",
    "actions": ["scale_up"],
    "resolved": True,
    "mttr": 5
}

bad_trajectory = {
    "incident": "cpu_spike",
    "actions": [
        "rollback",
        "rollback",
        "rollback",
        "rollback",
        "rollback"
    ],
    "resolved": False,
    "mttr": 25
}

average_trajectory = {
    "incident": "cpu_spike",
    "actions": [
        "restart_service",
        "restart_service",
        "scale_up"
    ],
    "resolved": True,
    "mttr": 15
}

print("\nGOOD")
print(judge.evaluate(good_trajectory))

print("\nAVERAGE")
print(judge.evaluate(average_trajectory))

print("\nBAD")
print(judge.evaluate(bad_trajectory))