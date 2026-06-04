# This module defines the state builder for the RL agent in the AIOps system.
# It combines system metrics, LLM analysis, and RAG retrieval results
# into a structured state representation for the agent.

# Action and incident mappings to convert categorical outputs into numerical values for the RL state representation.
ACTION_MAP={
    "recommend_restart_service":0,
    "recommend_scale_up":1,
    "recommend_clear_cache":2,
    "recommend_rollback":3,
    "recommend_dependency_check":4,
    "recommend_no_action":5
}

INCIDENT_MAP={
    "cpu_spike":0,
    "memory_leak":1,
    "service_crash":2,
    "db_latency":3,
    "dependency_failure":4
}

def build_state(metrics, llm_output, rag_output):
    # This function builds the state representation for the RL agent by combining the current system metrics,
    # the LLM's analysis of the incident, and the RAG engine's retrieval results.

    return [
        metrics["cpu"],
        metrics["memory"],
        metrics["latency"],
        metrics["error_rate"],

        INCIDENT_MAP[llm_output["root_cause"]],

        llm_output["confidence"],
        rag_output[0]["distance"]
    ]