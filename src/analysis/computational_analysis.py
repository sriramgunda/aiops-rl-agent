class ComputationalAnalysis:
    def __init__(self, performance):
        self.performance = performance

    def decision_pipeline(self):
        return {
            "Telemetry": self.performance["telemetry_latency_ms"]["average"],
            "RAG": self.performance["rag_latency_ms"]["average"],
            "RCA": self.performance["rca_latency_ms"]["average"],
            "State Builder": self.performance["state_builder_latency_ms"]["average"],
            "PPO": self.performance["ppo_inference_ms"]["average"],
            "Pipeline": self.performance["pipeline_latency_ms"]["average"]
        }