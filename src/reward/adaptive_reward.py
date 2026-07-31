from dataclasses import dataclass

@dataclass
class AdaptiveRewardConfig:
    alpha_min: float = 0.05
    alpha_max: float = 0.60
    confidence_power: float = 1.5

class AdaptiveReward:
    def __init__(self, config: AdaptiveRewardConfig = AdaptiveRewardConfig()):
        self.config = config

    def compute_alpha(self, confidence: float) -> float:
        """
        confidence will be in the range [0,1]
        High confidence  -> small alpha
        Low confidence   -> large alpha
        """
        confidence = max(0.0, min(1.0, confidence))

        alpha = (
            self.config.alpha_min
            +
            (self.config.alpha_max - self.config.alpha_min)
            * ((1.0 - confidence) ** self.config.confidence_power)
        )

        return alpha

    def hybrid_reward(
            self,
            env_reward: float,
            llm_reward: float,
            confidence: float):

        alpha = self.compute_alpha(confidence)
        #llm_reward = llm_score / 100.0
        reward = ((1.0 - alpha) * env_reward + alpha * llm_reward)

        return reward, alpha