"""
demo_engine.py

Workflow orchestration engine for the
Autonomous AI SRE Demonstration Platform.
"""

from __future__ import annotations

import time
from typing import Generator

from incident_factory import IncidentFactory
from scenario_repository import Scenario
# from telemetry_simulator import TelemetrySimulator
from workflow_state import (
    WorkflowStage,
    WorkflowState,
    Telemetry,
)

from src.environment.state_builder import build_state
from src.rag.retriever import IncidentRetriever
from src.rag.telemetry_translator import TelemetryTranslator
from pathlib import Path
from src.llm.rca_agent import RCAAgent
import numpy as np
from stable_baselines3 import PPO
from src.environment.actions import ACTIONS
from src.environment.aiops_env import AIOpsEnv

class DemoEngine:
    """
    Coordinates the end-to-end workflow.

    This class intentionally contains no business
    logic for RAG, PPO or RCA.

    It only orchestrates modules.
    """

    def __init__(self):
        self.env = AIOpsEnv(use_llm_reward=True, debug=False)

        self.factory = IncidentFactory()
        #self.telemetry = TelemetrySimulator()

        self.retriever = IncidentRetriever()
        knowledge_path = (Path(__file__).resolve().parents[2] / "data" / "incidents" / "historical_incidents.json")
        self.retriever.load(str(knowledge_path))

        self.rca = RCAAgent()

        self.ppo = PPO.load("results/ppo/ppo_llm_reward")

        

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def execute(
        self,
        scenario: Scenario,
        severity=None,
        delay: float = 0.7
    ) -> Generator[tuple[WorkflowStage, WorkflowState], None, WorkflowState]:
        """
        Execute the complete workflow.

        Yields every stage so Streamlit can
        progressively update the UI.
        """

        state = self.factory.create(scenario, severity)

        obs, _ = self.env.reset()
        # self.sync_environment(state)
        self.update_telemetry_from_env(state)

        # ----------------------------------
        # Stage 1
        # ----------------------------------
        state.current_stage = WorkflowStage.TELEMETRY
        self.update_telemetry_from_env(state)
        state.add_log("Telemetry", "Collecting telemetry from AIOps Environment.")
        state.add_console(f"CPU        : {state.telemetry.cpu_percent:.1f}")
        state.add_console(f"Memory     : {state.telemetry.memory_percent:.1f}")
        state.add_console(f"Latency    : {state.telemetry.latency_ms:.1f}")
        state.add_console(f"HTTP500    : {state.telemetry.http_500_errors}")
        yield WorkflowStage.TELEMETRY, state
        time.sleep(delay)

        # ----------------------------------
        # Stage 2
        # ----------------------------------
        state.current_stage = WorkflowStage.RAG
        yield WorkflowStage.RAG, state
        self.run_rag(state, scenario)
        time.sleep(delay)

        # ----------------------------------
        # Stage 3
        # ----------------------------------
        state.current_stage = WorkflowStage.RCA
        yield WorkflowStage.RCA, state
        self.run_rca(state, scenario)
        time.sleep(delay)

        # ----------------------------------
        # Stage 4
        # ----------------------------------      
        state.current_stage = WorkflowStage.STATE_BUILDER
        yield WorkflowStage.STATE_BUILDER, state
        self.build_state_vector(state)
        time.sleep(delay)

        # ----------------------------------
        # Stage 5
        # ----------------------------------
        state.current_stage = WorkflowStage.PPO
        yield WorkflowStage.PPO, state
        self.run_ppo(state, scenario)
        time.sleep(delay)

        # ----------------------------------
        # Stage 6
        # ----------------------------------

        for stage, updated_state in self.run_episode(state, delay):
            yield stage, updated_state

        # ----------------------------------
        # Stage 7
        # ----------------------------------
        state.current_stage = WorkflowStage.REWARD
        yield WorkflowStage.REWARD, state
        self.calculate_reward(state)
        time.sleep(delay)

        # ----------------------------------
        # Stage 8
        # ----------------------------------
        state.current_stage = WorkflowStage.RESOLUTION
        yield WorkflowStage.RESOLUTION, state
        self.resolve(state)
        state.completed = True
        yield WorkflowStage.RESOLUTION, state


    def build_state_vector(self, state: WorkflowState):
        t = state.telemetry
        INCIDENT_NAME_MAP = {
            "CPU Spike": "cpu_spike",
            "Memory Leak": "memory_leak",
            "Database Latency": "db_latency",
            "HTTP 500 Errors": "service_crash"
        }

        rca_deprecated = {
            "incident": INCIDENT_NAME_MAP[state.incident.incident_type],
            "confidence": 0.95,
            "recommended_action": "restart_service"
        }

        metrics_deprecated = {
            "cpu": t.cpu_percent,
            "memory": t.memory_percent,
            "latency": t.latency_ms,
            "error_rate": t.http_500_errors,
            "http_500": t.http_500_errors,
            "db_timeout": t.db_latency_ms,
            "upstream_timeout": t.network_loss_percent,
            "pod_restart": t.restart_count,
            # Temporary until PPO integration
            "recommended_action": 0
        }

        rca = {
            "incident": state.retrieved_incidents["document"]["incident"],
            "confidence": state.rca_result["confidence"],
            "recommended_action": state.rca_result["recommended_action"],
        }

        metrics = self.env.state.copy()

        state.state_vector = build_state(metrics, rca)

        state.add_log(
            "State Builder",
            "State vector generated using real environment.state_builder."
        )
        state.add_console(f"State Vector = {state.state_vector}")


    def run_rag(self, state: WorkflowState, scenario=None):
        t = state.telemetry
        metrics_deprecated = {
            "cpu": t.cpu_percent,
            "memory": t.memory_percent,
            "latency": t.latency_ms,
            "error_rate": t.http_500_errors,
            "http_500": t.http_500_errors > 0,
            "db_timeout": t.db_latency_ms > 500,
            "upstream_timeout": t.network_loss_percent > 5,
            "pod_restart": t.restart_count > 0
        }

        metrics = self.env.state

        query = TelemetryTranslator.to_text(metrics)

        result = self.retriever.retrieve(query)
        doc = result["document"]

        state.retrieved_incidents = result

        state.add_log(
            "Hybrid RAG",
            f"Retrieved '{doc['incident']}' (score={result['score']:.3f})"
        )

        state.add_console(f"Query = {query}")
        state.add_console(f"Similarity = {result['score']:.3f}")


    def run_rca(self, state: WorkflowState, scenario=None):

        result = self.rca.analyze(state.retrieved_incidents)
        state.rca_result = result

        state.add_log(
            "RCA",
            f"Root Cause: {result['root_cause']} "
            f"(confidence={result['confidence']:.3f})"
        )
        state.add_console(f"Root Cause = {result['root_cause']}")
        state.add_console(f"Recommended Action = {result['recommended_action']}")

    def run_ppo(self, state: WorkflowState, scenario=None):
        # obs = np.array(state.state_vector, dtype=np.float32)
        obs = self.env._obs()
        action, _ = self.ppo.predict(obs, deterministic=True)

        if isinstance(action, np.ndarray):
            action = int(action.item())

        state.ppo_result = {
            "action": action,
            "action_name": ACTIONS[action],
            "confidence": None
        }

        state.add_log(
            "PPO",
            f"Selected action: {ACTIONS[action]}"
        )
        state.add_console(f"PPO Action = {action}")
        state.add_console(f"Action Name = {ACTIONS[action]}")

    def run_episode(self, state, delay=0.7):
        from workflow_state import ExecutionResult
        import copy
        episode_reward = 0

        while True:
            before_metrics = copy.deepcopy(state.telemetry)
            obs = self.env._obs()

            action,_ = self.ppo.predict(obs, deterministic=True)

            if isinstance(action,np.ndarray):
                action = int(action.item())

            state.ppo_result = {
                "action": action,
                "action_name": ACTIONS[action],
                "confidence": None
            }

            state.add_log("Execution", f"Executing {ACTIONS[action]}")

            state.add_console("="*60)
            state.add_console("ENVIRONMENT BEFORE")
            state.add_console(f"CPU      : {before_metrics.cpu_percent}")
            state.add_console(f"Memory   : {before_metrics.memory_percent}")
            state.add_console(f"Latency  : {before_metrics.latency_ms}")
            state.add_console(f"HTTP500  : {before_metrics.http_500_errors}")

            obs,reward,done,_,info = self.env.step(action)

            self.update_telemetry_from_env(state)

            after_metrics = copy.deepcopy(state.telemetry)

            state.execution_result = ExecutionResult(
                before_metrics=before_metrics,
                after_metrics=after_metrics,
                execution_time_seconds=round(
                    info["latency"]["pipeline_latency_ms"]/1000,
                    3
                ),
                success=info["success"]
            )

            state.environment_reward = reward
            state.environment_info = info

            state.reward_history.append(
                {
                    "step": info["step"],
                    "action": ACTIONS[action],
                    "structured_reward": float(info.get("structured_reward", reward)),
                    "llm_reward": (
                        float(info["llm_score"])
                        if info.get("llm_score") is not None
                        else None
                    ),
                    "adaptive_alpha": (
                        float(info["adaptive_alpha"])
                        if info.get("adaptive_alpha") is not None
                        else None
                    ),
                    "hybrid_reward": float(reward),
                })

            info["episode_reward"] = episode_reward + reward

            episode_reward += reward

            state.add_console("")
            state.add_console("ACTION")
            state.add_console(ACTIONS[action])
            state.add_console("")
            state.add_console("ENVIRONMENT AFTER")
            state.add_console(f"CPU      : {after_metrics.cpu_percent}")
            state.add_console(f"Memory   : {after_metrics.memory_percent}")
            state.add_console(f"Latency  : {after_metrics.latency_ms}")
            state.add_console(f"HTTP500  : {after_metrics.http_500_errors}")
            state.add_console("")

            state.add_console(f"Reward : {reward:.2f}")
            state.add_log("Execution", f"Reward={reward:.2f}")

            state.current_stage = WorkflowStage.EXECUTION

            yield WorkflowStage.EXECUTION,state

            if done:
                break

        state.environment_reward = episode_reward
        state.add_console("="*60)
        state.add_console(f"Episode Reward : {episode_reward:.2f}")


    def execute_action(self, state):
        from workflow_state import ExecutionResult
        state.add_console("=" * 60)
        state.add_console("ENTER execute_action()")
        action = state.ppo_result["action"]
        state.add_console(f"PPO Action = {action}")

        obs, reward, done, _, info = self.env.step(action)
        import copy
        before_metrics = copy.deepcopy(state.telemetry)

        state.add_console("Returned from env.step()")
        state.add_console(f"Reward = {reward}")
        state.add_console(f"Done = {done}")
        state.add_console(f"Success = {info['success']}")

        state.environment_observation = obs
        state.environment_reward = reward
        state.environment_done = done
        state.environment_info = info

        self.update_telemetry_from_env(state)
        after_metrics = copy.deepcopy(state.telemetry)

        state.execution_result = ExecutionResult(
            #before_metrics = state.telemetry,
            #after_metrics = state.expected_after_telemetry,
            #after_metrics = state.telemetry,
            before_metrics = before_metrics,
            after_metrics = after_metrics,
            execution_time_seconds = round(info["latency"]["pipeline_latency_ms"] / 1000, 3),
            success = info["success"]
        )

        state.add_log(
            "Environment",
            f"Action '{info['action_name']}' executed"
        )     


    def calculate_reward(self, state):
        from workflow_state import RewardResult

        # info = state.environment_info

        latest = state.reward_history[-1]

        structured_reward = latest["structured_reward"]
        llm_reward = latest["llm_reward"]
        adaptive_alpha = latest["adaptive_alpha"]
        hybrid_reward = latest["hybrid_reward"]

        state.reward_result = RewardResult(
            structured_reward = structured_reward,
            llm_reward = llm_reward,
            adaptive_alpha = adaptive_alpha,
            final_reward = hybrid_reward,
        )

        state.add_console("")
        state.add_console("Reward Breakdown (Environment)")
        state.add_console("----------------")
        state.add_console(f"Structured : {structured_reward:.2f}")
        state.add_console(f"LLM        : {llm_reward:.2f}")
        state.add_console(f"Alpha      : {adaptive_alpha:.3f}")
        state.add_console(f"Hybrid     : {hybrid_reward:.2f}")
        state.add_console(f"Episode    : {state.environment_reward:.2f}")

    def resolve(self, state):
        from workflow_state import ResolutionResult
        info = state.environment_info

        state.resolution_result = ResolutionResult(
            resolved=info["success"],
            mttr_seconds=info["step"] * 5,
            confidence=state.rca_result["confidence"],
            #summary=(
            #    f"{state.ppo_result['action_name']} "
            #    f"{'resolved' if info['success'] else 'did not resolve'} "
            #    "the incident."
            #),
            summary = (
                    f"""
                Incident Successfully Resolved

                Incident
                ---------
                {state.incident.incident_type}

                Root Cause
                ----------
                {state.rca_result['root_cause']}

                Action
                ------
                {state.ppo_result['action_name']}

                Reward
                ------
                {state.environment_reward:.2f}

                Latency

                {state.execution_result.before_metrics.latency_ms:.0f} ms

                ↓

                {state.execution_result.after_metrics.latency_ms:.0f} ms

                HTTP500

                {state.execution_result.before_metrics.http_500_errors}

                ↓

                {state.execution_result.after_metrics.http_500_errors}
                """
            )
        )

        state.add_log(
            "Resolution",
            "Environment evaluation completed."
        )


    def sync_environment(self, state):
        """
        Synchronize the demo telemetry with the environment state.
        This makes the dashboard display the actual environment state.
        """

        env_state = self.env.state

        telemetry = state.telemetry
        telemetry.cpu_percent = env_state["cpu"]
        telemetry.memory_percent = env_state["memory"]
        telemetry.latency_ms = env_state["latency"]
        telemetry.http_500_errors = env_state["http_500"]
        telemetry.db_latency_ms = env_state["db_timeout"]
        telemetry.restart_count = env_state["pod_restart"]

        if hasattr(telemetry, "network_loss_percent"):
            telemetry.network_loss_percent = env_state["upstream_timeout"]


    def update_telemetry_from_env(self, state):
        env = self.env.state

        state.telemetry = Telemetry(
            cpu_percent=env["cpu"],
            memory_percent=env["memory"],
            latency_ms=env["latency"],
            http_500_errors=env["http_500"],
            db_latency_ms=env["db_timeout"],
            pod_count=env.get("pod_count",3),
            restart_count=env["pod_restart"],
            network_loss_percent=env["upstream_timeout"],
            disk_percent=env.get("disk",65),
            active_connections=env.get("connections", 250)
        )