# Log episode details
class EpisodeLogger:
    def __init__(self):
        self.episodes=[]
        
    def log(self, incident, reward, steps, success):
        self.episodes.append({
            "incident":incident,
            "reward":reward,
            "steps":steps,
            "success":success
        })