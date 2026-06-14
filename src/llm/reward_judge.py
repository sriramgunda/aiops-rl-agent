from ollama import chat
import re

class RewardJudge:
    def __init__(self, model="qwen2.5:7b"):
        self.model = model

    def evaluate(self, trajectory):
        prompt = f"""
You are a senior Site Reliability Engineer.

Evaluate the remediation trajectory.

Incident:
{trajectory['incident']}

Actions:
{trajectory['actions']}

Resolved:
{trajectory['resolved']}

MTTR:
{trajectory['mttr']}

Scoring Rules:

100 = excellent remediation

80 = good remediation

50 = acceptable

20 = poor remediation

0 = failed remediation

Return ONLY a number between 0 and 100.
"""
        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        score_text = (response["message"]["content"].strip())

        try:
            matches = re.findall(r"\d+\.?\d*", score_text)
            if matches:
                score = float(matches[0])
            else:
                score = 50

        except Exception:
            score = 50
        return score