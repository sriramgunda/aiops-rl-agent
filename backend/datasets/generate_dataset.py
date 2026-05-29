# This script generates a synthetic dataset of incidents based on the predefined INCIDENTS in the environment.
# It creates a CSV file with 500 rows, where each row represents an incident with its corresponding CPU, memory, latency, error rate, and incident type.

import pandas as pd
import random

# Ensure the backend parent directory is on sys.path so sibling packages like
# `environment` can be imported when running this script directly.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from environment.incidents import INCIDENTS

rows=[]
rows_length=500

for _ in range(rows_length):

    incident = random.choice(
        list(INCIDENTS.keys())
    )

    state = INCIDENTS[incident]

    rows.append({
        "cpu":state["cpu"],
        "memory":state["memory"],
        "latency":state["latency"],
        "error_rate":state["error_rate"],
        "incident":incident
    })

df = pd.DataFrame(rows)

# Save the dataset to a CSV file
df.to_csv(
"datasets/incidents/synthetic_incidents.csv",
index=False
)