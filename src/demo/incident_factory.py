"""
incident_factory.py

Creates realistic production incidents for the
Autonomous AI SRE Demonstration Platform.
"""

from __future__ import annotations

import random
import uuid
from datetime import datetime
from typing import List

from scenario_repository import Scenario
from workflow_state import (
    Incident,
    IncidentStatus,
    Severity,
    WorkflowState,
)


class IncidentFactory:
    """
    Creates enterprise-style production incidents.
    """

    REGIONS: List[str] = [
        "us-east-1",
        "us-west-2",
        "eu-west-1",
        "ap-south-1",
        "ap-southeast-1"
    ]

    CUSTOMERS: List[str] = [
        "Acme Bank",
        "Global Retail",
        "FinServe",
        "Enterprise Payments",
        "Northwind Financial"
    ]

    HOSTS: List[str] = [
        "worker-node-01",
        "worker-node-02",
        "worker-node-03",
        "worker-node-04",
        "worker-node-05"
    ]

    POD_PREFIX = [
        "payment-api",
        "customer-api",
        "order-service",
        "gateway",
        "notification-service"
    ]

    NAMESPACES = [
        "production",
        "payments",
        "banking",
        "retail"
    ]

    def create(
        self,
        scenario: Scenario,
        severity: Severity | None = None
    ) -> WorkflowState:
        """
        Create a new workflow state initialized
        with a realistic production incident.
        """

        severity = severity or scenario.default_severity

        incident = Incident(

            incident_id=self._generate_incident_id(),

            incident_type=scenario.name,

            application=scenario.application,

            environment=scenario.environment,

            severity=severity,

            region=random.choice(self.REGIONS),

            host=random.choice(self.HOSTS),

            description=scenario.description,

            created_time=datetime.utcnow(),

            status=IncidentStatus.OPEN
        )

        state = WorkflowState()

        state.incident = incident

        state.add_log(
            "SYSTEM",
            f"Incident {incident.incident_id} created."
        )

        state.add_log(
            "SYSTEM",
            f"Customer: {self.random_customer()}"
        )

        state.add_log(
            "SYSTEM",
            f"Namespace: {self.random_namespace()}"
        )

        state.add_log(
            "SYSTEM",
            f"Pod: {self.random_pod_name()}"
        )

        return state

    # --------------------------------------------------
    # Helper Methods
    # --------------------------------------------------

    @staticmethod
    def _generate_incident_id() -> str:
        """
        Example:
            INC-83AF1D
        """

        return f"INC-{uuid.uuid4().hex[:6].upper()}"

    @staticmethod
    def random_customer() -> str:
        return random.choice(
            IncidentFactory.CUSTOMERS
        )

    @staticmethod
    def random_namespace() -> str:
        return random.choice(
            IncidentFactory.NAMESPACES
        )

    @staticmethod
    def random_pod_name() -> str:

        prefix = random.choice(
            IncidentFactory.POD_PREFIX
        )

        suffix = uuid.uuid4().hex[:5]

        return f"{prefix}-{suffix}"

    @staticmethod
    def random_node() -> str:
        return random.choice(
            IncidentFactory.HOSTS
        )