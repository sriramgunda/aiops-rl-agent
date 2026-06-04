# This file defines a hybrid reward function that combines
# structured reward based on system metrics
# and a reward judged by a large language model.
from reward_engine.structured_reward import structured_reward
from reward_engine.llm_reward import judge_reward
from dotenv import load_dotenv
import os

load_dotenv()

STRUCTURED_WEIGHT = float(os.getenv("STRUCTURED_WEIGHT"))
LLM_WEIGHT = 1 - STRUCTURED_WEIGHT

def hybrid_reward(incident, action, before, after, action_reward):
    # Calculate the structured reward and the LLM reward,
    # then combine them using the defined weights.
    sr = structured_reward(before, after, action_reward)
    llm = judge_reward(incident, action, before, after)

    final = (STRUCTURED_WEIGHT * sr + LLM_WEIGHT * llm["reward"])

    return {
        "reward":final,
        "structured":sr,
        "llm":llm
    }