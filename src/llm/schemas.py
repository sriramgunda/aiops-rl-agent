from pydantic import BaseModel
from typing import List


class TrajectoryStep(BaseModel):
    action: str
    reward: float


class Trajectory(BaseModel):
    incident: str
    steps: List[TrajectoryStep]
    resolved: bool
    mttr: float