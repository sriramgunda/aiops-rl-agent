import random

class IncidentGenerator:
    # Simulate different types of incidents with varying severity and characteristics
    INCIDENTS = [
        "cpu_spike",
        "memory_leak",
        "service_crash",
        "db_latency",
        "dependency_failure"
    ]

    def generate(self):
        incident = random.choice(self.INCIDENTS)
        # Generate incident characteristics based on the type of incident
        if incident == "cpu_spike":
            return {
                "incident": incident,
                "cpu": random.randint(85,100),
                "memory": random.randint(40,70),
                "latency": random.randint(200,500),
                "error_rate": random.randint(5,20)
            }

        elif incident == "memory_leak":
            return {
                "incident": incident,
                "cpu": random.randint(40,70),
                "memory": random.randint(85,100),
                "latency": random.randint(150,350),
                "error_rate": random.randint(10,25)
            }

        elif incident == "service_crash":
            return {
                "incident": incident,
                "cpu": random.randint(10,40),
                "memory": random.randint(20,50),
                "latency": random.randint(400,900),
                "error_rate": random.randint(70,100)
            }

        elif incident == "db_latency":
            return {
                "incident": incident,
                "cpu": random.randint(30,60),
                "memory": random.randint(30,60),
                "latency": random.randint(700,1200),
                "error_rate": random.randint(20,50)
            }

        return {
            "incident": incident,
            "cpu": random.randint(60,90),
            "memory": random.randint(50,80),
            "latency": random.randint(500,1000),
            "error_rate": random.randint(40,80)
        }