import random
import numpy as np

class IncidentGenerator:
    # Simulate different types of incidents with varying severity and characteristics
    INCIDENTS = [
        "cpu_spike",
        "memory_leak",
        "service_crash",
        "db_latency",
        "dependency_failure"
    ]

    def __init__(self):
        self.rng = np.random.default_rng()

    def set_seed(self, seed):
        self.rng = np.random.default_rng(seed)

    def generate(self):
        incident = str(self.rng.choice(self.INCIDENTS))
        # Generate incident characteristics based on the type of incident
        if incident == "cpu_spike":
            return {
                "incident": incident,
                "cpu": int(self.rng.integers(85,100)),
                "memory": int(self.rng.integers(40,70)),
                "latency": int(self.rng.integers(200,500)),
                "error_rate": int(self.rng.integers(5,20)),
                "http_500":0,
                "db_timeout":0,
                "upstream_timeout":0,
                "pod_restart":0,
                "recommended_action": 1
            }

        elif incident == "memory_leak":
            return {
                "incident": incident,
                "cpu": int(self.rng.integers(40,70)),
                "memory": int(self.rng.integers(85,100)),
                "latency": int(self.rng.integers(150,350)),
                "error_rate": int(self.rng.integers(10,25)),
                "http_500":0,
                "db_timeout":0,
                "upstream_timeout":0,
                "pod_restart":1,
                "recommended_action": 5
            }

        elif incident == "service_crash":
            return {
                "incident": incident,
                "cpu": int(self.rng.integers(10,40)),
                "memory": int(self.rng.integers(20,50)),
                "latency": int(self.rng.integers(400,900)),
                "error_rate": int(self.rng.integers(70,100)),
                "http_500":1,
                "db_timeout":0,
                "upstream_timeout":0,
                "pod_restart":1,
                "recommended_action": 5
            }

        elif incident == "db_latency":
            return {
                "incident": incident,
                "cpu": int(self.rng.integers(30,60)),
                "memory": int(self.rng.integers(30,60)),
                "latency": int(self.rng.integers(700,1200)),
                "error_rate": int(self.rng.integers(20,50)),
                "http_500":0,
                "db_timeout":1,
                "upstream_timeout":0,
                "pod_restart":0,
                "recommended_action": 2
            }

        elif incident == "dependency_failure":
            return {
                "incident": incident,
                "cpu":int(self.rng.integers(60,90)),
                "memory":int(self.rng.integers(50,80)),
                "latency":int(self.rng.integers(500,1000)),
                "error_rate":int(self.rng.integers(40,80)),
                "http_500":0,
                "db_timeout":0,
                "upstream_timeout":1,
                "pod_restart":0,
                "recommended_action": 4
            }

        return {
            "incident": incident,
            "cpu": int(self.rng.integers(60,90)),
            "memory": int(self.rng.integers(50,80)),
            "latency": int(self.rng.integers(500,1000)),
            "error_rate": int(self.rng.integers(40,80)),
            "http_500": int(self.rng.integers(0,1)),
            "db_timeout": int(self.rng.integers(0,1)),
            "upstream_timeout": int(self.rng.integers(0,1)),
            "pod_restart": int(self.rng.integers(0,1)),
            "recommended_action": 0
        }