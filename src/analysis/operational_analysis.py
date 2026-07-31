class OperationalAnalysis:
    def __init__(self, report):
        self.report = report

    def summary(self):
        return {
            "Success Rate": self.report["success_rate"],
            "MTTR": self.report["mttr_minutes"],
            "Average Reward": self.report["avg_reward"],
            "Recommendation Follow Rate": self.report["recommendation_follow_rate"],
            "Episode Latency": self.report["performance"]["episode_latency_ms"]["average"]
        }