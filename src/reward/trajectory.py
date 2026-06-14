class Trajectory:
    def __init__(self):
        self.steps = []

    def add_step(self, state, action, reward):
        self.steps.append({
            "state": state,
            "action": action,
            "reward": reward
        })

    def summary(self, incident, resolved, mttr):
        return {
            "incident": incident,
            "steps": self.steps,
            "resolved": resolved,
            "mttr": mttr
        }