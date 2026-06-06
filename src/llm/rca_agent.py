class RCAAgent:
    def analyze(self, retrieved):
        doc = retrieved["document"]
        return {
            "incident": doc["incident"],
            "confidence": 1.0/(1.0 +retrieved["distance"]),
            "root_cause": doc["root_cause"],
            "recommended_action": doc["recommended_action"]
        }