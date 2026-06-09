from src.environment.incident_generator import IncidentGenerator

from src.rag.telemetry_translator import TelemetryTranslator

from src.rag.retriever import IncidentRetriever

generator = IncidentGenerator()

retriever = IncidentRetriever()

retriever.load("data/incidents/historical_incidents.json")

rca_success_rate = 0
total_tests_runs = 100

for i in range(total_tests_runs):
    state = generator.generate()
    query = TelemetryTranslator.to_text(state)

    result = retriever.retrieve(query)

    print("\n-------------------")
    print("True Incident:", state["incident"])
    print("Query:", query)
    print("Predicted:", result["document"]["incident"])

    if state["incident"] == result["document"]["incident"]:
        rca_success_rate += 1
    
rca_accuracy = (rca_success_rate / total_tests_runs) * 100
print("\n-------------------")
print(f"RCA Accuracy: {rca_accuracy}%")