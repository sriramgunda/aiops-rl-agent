import random

from incidents import INCIDENTS

class AIOpsSimulator:

    def generate_incident(self):
        # Randomly select an incident type and return its details
        incident=random.choice(list(INCIDENTS.keys()))
        print(f"Generated incident: {incident}")
        return incident, INCIDENTS[incident]