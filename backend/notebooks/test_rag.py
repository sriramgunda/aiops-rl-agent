import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rag.rag_engine import RAGEngine

rag = RAGEngine()

rag.load_documents(
"datasets/runbooks/historical_incidents.json"
)

query = "CPU very high latency increasing"

results = rag.retrieve(query)

print(results)