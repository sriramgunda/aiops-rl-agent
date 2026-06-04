import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import ollama
import os

from openai import OpenAI

from dotenv import load_dotenv

# load environment variables from a .env file into os.environ
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "test")

client = OpenAI(api_key=OPENAI_API_KEY)
MODEL = os.getenv("RCA_MODEL", "qwen2.5:7b")

def analyze_incident(state, retrieved_context):

    prompt=f"""

You are an SRE incident analyst.
System state:
{state}

Historical incidents:
{retrieved_context}

Identify:
1. probable root cause
2. recommended remediation

Respond JSON only.

{{
"root_cause":"cpu_spike|memory_leak|service_crash|db_latency|dependency_failure",

"confidence":0.0,

"recommended_action":
"recommend_restart_service|
recommend_scale_up|
recommend_clear_cache|
recommend_rollback|
recommend_dependency_check|
recommend_no_action"

}}

"""

    if os.getenv("LLM_PROVIDER") == "openai":
        response = client.chat.completions.create(
            model=MODEL,
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
        try:
            content = response["message"]["content"]
        except KeyError:
            print("Unexpected response format from Ollama:", response)
            raise
        except Exception as e:
            print("Error processing Ollama response:", e)
            raise
        return json.loads(content)