# Translate raw metricsnumbers to text formatted
# to help RAG symantic search work efficiently
class TelemetryTranslator:
    @staticmethod
    def to_text(state):
        symptoms = []

        # cpu spike
        if state["cpu"] > 85:
            symptoms.append("high cpu utilization")
            symptoms.append("application slowdown")
        
        # memory leak
        if state["memory"] > 85:
            symptoms.append("high memory consumption")
            symptoms.append("memory exhaustion")
        
        # latency issue
        if state["latency"] > 700:
            symptoms.append("query timeout")
        elif state["latency"] > 300:
            symptoms.append("application slowdown")
        
        # error rates
        if state["error_rate"] > 70:
            symptoms.append("service unavailable")
        elif state["error_rate"] > 5:
            symptoms.append("traffic surge")
        
        # http 500 errors
        if state["http_500"]:
            symptoms.append("500 errors")
        
        # database connection errors, timeout issues
        if state["db_timeout"]:
            symptoms.append("database timeout")
        
        # upstream dependency issues
        if state["upstream_timeout"]:
            symptoms.append("upstream timeout")
        
        # pod availability interruptions
        if state["pod_restart"]:
            symptoms.append("pod restart")

        return ", ".join(symptoms)