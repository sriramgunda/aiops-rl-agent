"""
scenario_repository.py

Repository of predefined production incident scenarios used by the
Autonomous AI SRE Demonstration Platform.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from workflow_state import Severity


# ==========================================================
# Scenario Definition
# ==========================================================

@dataclass
class Scenario:

    name: str

    description: str

    application: str

    environment: str

    default_severity: Severity

    telemetry_before: Dict

    telemetry_after: Dict

    expected_root_cause: str

    alternative_root_causes: Dict[str, float]

    expected_action: str

    candidate_actions: Dict[str, float]

    structured_reward: float

    llm_reward: float

    adaptive_alpha: float


# ==========================================================
# Repository
# ==========================================================

SCENARIOS: Dict[str, Scenario] = {

    # ======================================================
    # Memory Leak
    # ======================================================

    "Memory Leak": Scenario(

        name="Memory Leak",

        description="Gradual JVM memory consumption resulting in application slowdown.",

        application="Payment API",

        environment="Kubernetes Cluster",

        default_severity=Severity.HIGH,

        telemetry_before={

            "cpu_percent":22,

            "memory_percent":94,

            "latency_ms":182,

            "http_500_errors":0,

            "db_latency_ms":43,

            "pod_count":6,

            "restart_count":0,

            "network_loss_percent":0.2,

            "disk_percent":41,

            "active_connections":850

        },

        telemetry_after={

            "cpu_percent":18,

            "memory_percent":57,

            "latency_ms":71,

            "http_500_errors":0,

            "db_latency_ms":38,

            "pod_count":6,

            "restart_count":0,

            "network_loss_percent":0.2,

            "disk_percent":41,

            "active_connections":842

        },

        expected_root_cause="Cache Growth",

        alternative_root_causes={

            "Memory Leak":0.08,

            "Heap Fragmentation":0.04

        },

        expected_action="Clear Cache",

        candidate_actions={

            "Restart Service":0.17,

            "Scale Up":0.08,

            "Clear Cache":0.72,

            "Rollback":0.03

        },

        structured_reward=40,

        llm_reward=18,

        adaptive_alpha=0.72
    ),

    # ======================================================
    # CPU Spike
    # ======================================================

    "CPU Spike": Scenario(

        name="CPU Spike",

        description="Unexpected increase in CPU utilization due to traffic surge.",

        application="Customer Portal",

        environment="Kubernetes Cluster",

        default_severity=Severity.HIGH,

        telemetry_before={

            "cpu_percent":98,

            "memory_percent":42,

            "latency_ms":420,

            "http_500_errors":7,

            "db_latency_ms":61,

            "pod_count":8,

            "restart_count":0,

            "network_loss_percent":0.3,

            "disk_percent":38,

            "active_connections":2900

        },

        telemetry_after={

            "cpu_percent":46,

            "memory_percent":44,

            "latency_ms":92,

            "http_500_errors":0,

            "db_latency_ms":44,

            "pod_count":10,

            "restart_count":0,

            "network_loss_percent":0.2,

            "disk_percent":39,

            "active_connections":2800

        },

        expected_root_cause="Traffic Surge",

        alternative_root_causes={

            "Runaway Process":0.09,

            "Autoscaler Delay":0.05

        },

        expected_action="Scale Up",

        candidate_actions={

            "Restart Service":0.05,

            "Scale Up":0.81,

            "Rollback":0.04,

            "Clear Cache":0.10

        },

        structured_reward=39,

        llm_reward=17,

        adaptive_alpha=0.69
    ),

    # ======================================================
    # HTTP 500 Errors
    # ======================================================

    "HTTP 500 Errors": Scenario(

        name="HTTP 500 Errors",

        description="High internal server error rate after deployment.",

        application="Payment Gateway",

        environment="AWS EC2",

        default_severity=Severity.CRITICAL,

        telemetry_before={

            "cpu_percent":34,

            "memory_percent":51,

            "latency_ms":610,

            "http_500_errors":42,

            "db_latency_ms":55,

            "pod_count":4,

            "restart_count":2,

            "network_loss_percent":0.1,

            "disk_percent":35,

            "active_connections":1450

        },

        telemetry_after={

            "cpu_percent":28,

            "memory_percent":47,

            "latency_ms":86,

            "http_500_errors":0,

            "db_latency_ms":41,

            "pod_count":4,

            "restart_count":2,

            "network_loss_percent":0.1,

            "disk_percent":35,

            "active_connections":1432

        },

        expected_root_cause="Application Deployment Failure",

        alternative_root_causes={

            "Configuration Error":0.14,

            "Dependency Failure":0.06

        },

        expected_action="Restart Service",

        candidate_actions={

            "Restart Service":0.75,

            "Rollback":0.18,

            "Scale Up":0.04,

            "Clear Cache":0.03

        },

        structured_reward=42,

        llm_reward=19,

        adaptive_alpha=0.74
    ),

    # ======================================================
    # Database Latency
    # ======================================================

    "Database Latency": Scenario(

        name="Database Latency",

        description="Database response time increases due to connection pool exhaustion.",

        application="Order Service",

        environment="Azure AKS",

        default_severity=Severity.HIGH,

        telemetry_before={

            "cpu_percent":19,

            "memory_percent":41,

            "latency_ms":540,

            "http_500_errors":3,

            "db_latency_ms":812,

            "pod_count":5,

            "restart_count":0,

            "network_loss_percent":0.2,

            "disk_percent":48,

            "active_connections":5000

        },

        telemetry_after={

            "cpu_percent":20,

            "memory_percent":40,

            "latency_ms":102,

            "http_500_errors":0,

            "db_latency_ms":96,

            "pod_count":5,

            "restart_count":0,

            "network_loss_percent":0.2,

            "disk_percent":48,

            "active_connections":2800

        },

        expected_root_cause="Connection Pool Exhaustion",

        alternative_root_causes={

            "Slow Queries":0.11,

            "Index Fragmentation":0.07

        },

        expected_action="Increase Connection Pool",

        candidate_actions={

            "Increase Connection Pool":0.79,

            "Restart Database Proxy":0.14,

            "Scale Up":0.05,

            "Rollback":0.02

        },

        structured_reward=41,

        llm_reward=18,

        adaptive_alpha=0.71
    )
}


# ==========================================================
# Helper Functions
# ==========================================================

def get_scenario(name: str) -> Scenario:
    """
    Retrieve a scenario by name.
    """
    return SCENARIOS[name]


def list_scenarios() -> List[str]:
    """
    Return all available scenario names.
    """
    return sorted(SCENARIOS.keys())