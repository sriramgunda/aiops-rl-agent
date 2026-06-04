# This file defines the reward engine that uses a large language model
# to evaluate the quality of remediation actions.
import json
import ollama
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = os.getenv("REWARD_JUDGE_MODEL")
USE_LLM = os.getenv("USE_LLM", "true").lower() == "true"

def judge_reward(incident, action, before, after):
    if not USE_LLM:
        print("LLM reward disabled, returning default reward")
        return {"reward": 0.5, "reason": "LLM usage disabled"}
    
    # This function constructs a prompt with the incident details,
    # the action taken, and the system state before and after the action.
    # It then sends this prompt to the LLM and expects a JSON response
    # containing the reward
    prompt=f"""

Incident:
{incident}

Action:
{action}

Before:
{before}

After:
{after}

Evaluate remediation quality.
Return JSON ONLY.

{{
"reward":float,
"reason":"..."
}}

"""

    response = ollama.chat(
        model=MODEL,
        messages=[
        {
            "role":"user",
            "content":prompt
        }]
    )
    print(f"LLM response: {response}")
    content = response["message"]["content"]

    def _extract_json_from_text(text: str):
        # Try direct parse first
        try:
            return json.loads(text)
        except Exception:
            pass

        # Try to find a fenced code block with JSON
        import re
        m = re.search(r'```(?:json)?\s*(\{.*\})\s*```', text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass

        # Fallback: find first { and last } and try to parse that slice
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            candidate = text[start:end+1]
            try:
                return json.loads(candidate)
            except Exception:
                pass

        raise ValueError("Could not extract JSON from LLM response")

    try:
        return _extract_json_from_text(content)
    except Exception as e:
        print(f"Failed to parse LLM JSON: {e}")
        return {"reward": 0.0, "reason": "invalid LLM response", "raw": content}