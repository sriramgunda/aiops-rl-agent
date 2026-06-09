from src.rag.retriever import IncidentRetriever

retriever = IncidentRetriever()

retriever.load("data/incidents/historical_incidents.json")

queries = [
    "high cpu utilization",
    "high memory consumption",
    "service unavailable",
    "database response delay",
    "upstream timeout",
    "application slowdown",
    "traffic surge",
    ""
]

for q in queries:
    print(f"\nQuery: {q}")
    result = retriever.retrieve(q)    
    print(f"RESULT: {result}")