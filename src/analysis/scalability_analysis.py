class ScalabilityAnalysis:
    def __init__(self, report):
        self.report = report

    def throughput(self):
        episode_latency = (self.report["performance"]["episode_latency_ms"]["average"])
        episodes_per_second = (1000 / episode_latency)

        return {
            "Episodes/sec": episodes_per_second,
            "Incidents/hour": episodes_per_second * 3600,
            "Incidents/day": episodes_per_second * 86400
        }

    def resources(self):
        perf = self.report["performance"]
        return {
            "CPU": perf["cpu_percent"]["average"],
            "Memory": perf["memory_mb"]["average"]
        }