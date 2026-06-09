class RCAAgent:
    def analyze(self, retrieved):
        doc = retrieved["document"]
        return {
            "incident": doc["incident"],
            "confidence": retrieved["score"],
            "root_cause": doc["root_cause"],
            "recommended_action": doc["recommended_action"]
        }