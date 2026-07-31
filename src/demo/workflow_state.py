"""
workflow_state.py

Shared data models for the Autonomous AI SRE Demo Platform.

Author : Sriram Gunda Dissertation Project
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


# ============================================================
# Enumerations
# ============================================================

class Severity(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class IncidentStatus(Enum):
    OPEN = "Open"
    INVESTIGATING = "Investigating"
    MITIGATING = "Mitigating"
    RESOLVED = "Resolved"


class WorkflowStage(Enum):
    TELEMETRY = "Telemetry Collection"
    STATE_BUILDER = "State Builder"
    RAG = "RAG Retrieval"
    RCA = "Root Cause Analysis"
    PPO = "PPO Decision"
    EXECUTION = "Action Execution"
    REWARD = "Reward Evaluation"
    RESOLUTION = "Incident Resolution"


# ============================================================
# Incident
# ============================================================

@dataclass
class Incident:

    incident_id: str

    incident_type: str

    application: str

    environment: str

    severity: Severity

    region: str

    host: str

    description: str

    created_time: datetime = field(default_factory=datetime.utcnow)

    status: IncidentStatus = IncidentStatus.OPEN


# ============================================================
# Telemetry
# ============================================================

@dataclass
class Telemetry:

    cpu_percent: float

    memory_percent: float

    latency_ms: float

    http_500_errors: int

    db_latency_ms: float

    pod_count: int

    restart_count: int

    network_loss_percent: float

    disk_percent: float

    active_connections: int


# ============================================================
# Retrieved Incident (RAG)
# ============================================================

@dataclass
class RetrievedIncident:

    incident_id: str

    root_cause: str

    resolution: str

    similarity_score: float


# ============================================================
# RCA Result
# ============================================================

@dataclass
class RCAResult:

    predicted_root_cause: str

    confidence: float

    alternatives: Dict[str, float]


# ============================================================
# PPO Result
# ============================================================

@dataclass
class PPOResult:

    selected_action: str

    confidence: float

    action_probabilities: Dict[str, float]


# ============================================================
# Execution Result
# ============================================================

@dataclass
class ExecutionResult:

    before_metrics: Telemetry

    after_metrics: Telemetry

    execution_time_seconds: float

    success: bool


# ============================================================
# Reward
# ============================================================

@dataclass
class RewardResult:

    structured_reward: float

    llm_reward: float

    adaptive_alpha: float

    final_reward: float


# ============================================================
# Resolution
# ============================================================

@dataclass
class ResolutionResult:

    resolved: bool

    mttr_seconds: float

    confidence: float

    summary: str


# ============================================================
# Log Entry
# ============================================================

@dataclass
class WorkflowLog:

    timestamp: datetime

    stage: str

    message: str


# ============================================================
# Complete Workflow State
# ============================================================

@dataclass
class WorkflowState:

    incident: Optional[Incident] = None

    telemetry: Optional[Telemetry] = None

    state_vector: List[float] = field(default_factory=list)

    retrieved_incidents: List[RetrievedIncident] = field(default_factory=list)

    rca_result: Optional[RCAResult] = None

    ppo_result: Optional[PPOResult] = None

    execution_result: Optional[ExecutionResult] = None

    environment_reward: float = 0.0

    environment_info: dict = field(default_factory=dict)

    environment_observation: list = field(default_factory=list)

    reward_result: Optional[RewardResult] = None

    resolution_result: Optional[ResolutionResult] = None

    logs: List[WorkflowLog] = field(default_factory=list)

    current_stage: WorkflowStage = WorkflowStage.TELEMETRY

    completed: bool = False

    expected_after_telemetry: Optional[Telemetry] = None

    console_logs: list[str] = field(default_factory=list)

    reward_history: list = field(default_factory=list)

    def add_log(
        self,
        stage: str,
        message: str
    ) -> None:
        """
        Add workflow log entry.
        """

        self.logs.append(
            WorkflowLog(
                timestamp=datetime.utcnow(),
                stage=stage,
                message=message
            )
        )

    def reset(self) -> None:
        """
        Reset workflow state.
        """

        self.incident = None
        self.telemetry = None
        self.state_vector = []

        self.retrieved_incidents = []

        self.rca_result = None

        self.ppo_result = None

        self.execution_result = None

        self.reward_result = None

        self.resolution_result = None

        self.logs.clear()

        self.completed = False

        self.current_stage = WorkflowStage.TELEMETRY
        self.expected_after_telemetry = None

    def add_console(self, message: str):
        self.console_logs.append(message)