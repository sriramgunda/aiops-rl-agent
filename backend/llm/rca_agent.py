import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from openai import OpenAI

client=OpenAI()

def analyze_incident(state, retrieved_context):

    prompt=f"""

System state:

{state}

Historical incidents:

{retrieved_context}

Identify:

1. probable root cause

2. recommended remediation

Respond JSON only.

"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
        {
            "role":"user",
            "content":prompt
        }
        ]
    )

    return response.choices[0].message.content