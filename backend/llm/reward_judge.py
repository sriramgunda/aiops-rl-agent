import ollama
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "test")
client = OpenAI(api_key=OPENAI_API_KEY)

MODEL = os.getenv("REWARD_JUDGE_MODEL", "llama3.1:8b")

def judge_trajectory(trajectory):

    prompt=f"""

You are an expert SRE evaluator.
Evaluate remediation quality.

Trajectory:
{trajectory}

Return score between 0 and 1.

Return JSON ONLY.

{{
"reward":float,
"reason":"..."
}}

"""
    if os.getenv("LLM_PROVIDER") == "openai":
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            messages=[
            {
                "role":"user",
                "content":prompt
            }
            ]
        )
        return response.choices[0].message.content
    
    if os.getenv("LLM_PROVIDER") == "ollama":
        response = ollama.chat(
            model=MODEL,
            messages=[
            {
                "role":"user",
                "content":prompt
            }
            ]
        )
        return response["message"]["content"]