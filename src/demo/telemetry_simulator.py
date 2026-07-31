"""
telemetry_simulator.py

Generates realistic production telemetry for demo incidents.
"""

from __future__ import annotations

import random
from copy import deepcopy

from scenario_repository import Scenario
from workflow_state import (
    Telemetry,
    WorkflowStage,
    WorkflowState,
)


class TelemetrySimulator:
    """
    Simulates production telemetry by applying small random
    variations to the baseline scenario metrics.
    """

    def __init__(self):

        self.cpu_variation = 2.0
        self.memory_variation = 2.0
        self.latency_variation = 15.0
        self.db_latency_variation = 20.0
        self.connections_variation = 100

    # -----------------------------------------------------
    # Public API
    # -----------------------------------------------------

    def collect(
        self,
        state: WorkflowState,
        scenario: Scenario
    ) -> WorkflowState:
        """
        Populate WorkflowState with telemetry collected from
        the selected scenario.
        """

        before = self._build_before_metrics(scenario)

        after = self._build_after_metrics(scenario)

        state.telemetry = before

        # Store expected "after" metrics for executor
        state.expected_after_telemetry = after

        state.current_stage = WorkflowStage.TELEMETRY

        state.add_log(
            "Telemetry",
            "Collecting infrastructure metrics..."
        )

        state.add_log(
            "Telemetry",
            f"CPU Usage        : {before.cpu_percent:.1f}%"
        )

        state.add_log(
            "Telemetry",
            f"Memory Usage     : {before.memory_percent:.1f}%"
        )

        state.add_log(
            "Telemetry",
            f"Latency          : {before.latency_ms:.1f} ms"
        )

        state.add_log(
            "Telemetry",
            f"HTTP 500 Errors  : {before.http_500_errors}"
        )

        state.add_log(
            "Telemetry",
            f"Database Latency : {before.db_latency_ms:.1f} ms"
        )

        state.add_log(
            "Telemetry",
            "Telemetry collection completed."
        )

        return state

    # -----------------------------------------------------
    # Before Metrics
    # -----------------------------------------------------

    def _build_before_metrics(
        self,
        scenario: Scenario
    ) -> Telemetry:

        data = deepcopy(scenario.telemetry_before)

        return Telemetry(

            cpu_percent=self._vary(
                data["cpu_percent"],
                self.cpu_variation
            ),

            memory_percent=self._vary(
                data["memory_percent"],
                self.memory_variation
            ),

            latency_ms=self._vary(
                data["latency_ms"],
                self.latency_variation
            ),

            http_500_errors=max(
                0,
                int(
                    self._vary(
                        data["http_500_errors"],
                        2
                    )
                )
            ),

            db_latency_ms=self._vary(
                data["db_latency_ms"],
                self.db_latency_variation
            ),

            pod_count=data["pod_count"],

            restart_count=data["restart_count"],

            network_loss_percent=round(
                self._vary(
                    data["network_loss_percent"],
                    0.15
                ),
                2
            ),

            disk_percent=self._vary(
                data["disk_percent"],
                2
            ),

            active_connections=int(
                self._vary(
                    data["active_connections"],
                    self.connections_variation
                )
            )
        )

    # -----------------------------------------------------
    # After Metrics
    # -----------------------------------------------------

    def _build_after_metrics(
        self,
        scenario: Scenario
    ) -> Telemetry:

        data = deepcopy(scenario.telemetry_after)

        return Telemetry(

            cpu_percent=self._vary(
                data["cpu_percent"],
                1
            ),

            memory_percent=self._vary(
                data["memory_percent"],
                1
            ),

            latency_ms=self._vary(
                data["latency_ms"],
                5
            ),

            http_500_errors=data["http_500_errors"],

            db_latency_ms=self._vary(
                data["db_latency_ms"],
                5
            ),

            pod_count=data["pod_count"],

            restart_count=data["restart_count"],

            network_loss_percent=data[
                "network_loss_percent"
            ],

            disk_percent=data["disk_percent"],

            active_connections=int(
                self._vary(
                    data["active_connections"],
                    25
                )
            )
        )

    # -----------------------------------------------------
    # Utility
    # -----------------------------------------------------

    @staticmethod
    def _vary(
        value: float,
        variation: float
    ) -> float:
        """
        Apply symmetric random variation around a value.
        """

        return round(
            random.uniform(
                value - variation,
                value + variation
            ),
            2
        )