import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.rag_engine import RAGEngine
from llm.rca_agent import analyze_incident

rag = RAGEngine()

rag.load_documents(
"backend/datasets/runbooks/historical_incidents.json"
)

state={
    "cpu":95,
    "memory":60,
    "latency":220,
    "error_rate":10
}

query = "cpu high latency"

retrieved = rag.retrieve(query)

response = analyze_incident(state, retrieved)

print(response)