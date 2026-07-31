"""
ui_renderer.py

Streamlit UI renderer for the Autonomous AI SRE Demo.

Responsibilities
----------------
- Render incident information
- Render telemetry
- Render workflow progress
- Render PPO/RAG/RCA outputs
- Render execution and rewards
- Render logs

No business logic should be implemented here.
"""

from __future__ import annotations

from typing import List

import pandas as pd
import streamlit as st

from workflow_state import (
    WorkflowState,
    WorkflowStage,
)


class UIRenderer:
    """
    Responsible for rendering the Streamlit dashboard.
    """

    def __init__(self):

        self.summary_placeholder = None
        self.telemetry_placeholder = None
        self.workflow_placeholder = None
        self.details_placeholder = None
        self.logs_placeholder = None

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def initialize(self):
        """
        Create dashboard placeholders only once.
        """

        st.set_page_config(
            page_title="Autonomous AI SRE",
            page_icon="🤖",
            layout="wide",
        )

        st.title("🤖 Autonomous AI SRE Platform")
        st.caption(
            "PPO + Hybrid RAG + Root Cause Analysis + Adaptive Reward Learning"
        )

        self.summary_placeholder = st.empty()
        self.telemetry_placeholder = st.empty()
        self.workflow_placeholder = st.empty()
        self.details_placeholder = st.empty()
        self.logs_placeholder = st.empty()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def render_dashboard(self, state: WorkflowState):

        self.render_incident_summary(state)

        self.render_telemetry(state)

        self.render_workflow(state)

        self.render_details(state)

        self.render_logs(state)

    # ---------------------------------------------------------
    # Incident Summary
    # ---------------------------------------------------------

    def render_incident_summary(self, state: WorkflowState):

        incident = state.incident

        with self.summary_placeholder.container():
            st.subheader("🚨 Incident")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Incident", incident.incident_id)
            c2.metric("Application", incident.application)
            c3.metric("Severity", incident.severity.name)
            c4.metric("Environment", incident.environment)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Region", incident.region)
            c2.metric("Host", incident.host)
            c3.metric("Status", incident.status.name)
            c4.metric("Type", incident.incident_type)

            st.info(incident.description)

    # ---------------------------------------------------------
    # Telemetry
    # ---------------------------------------------------------

    def render_telemetry(self, state: WorkflowState):

        t = state.telemetry

        if t is None:
            return

        with self.telemetry_placeholder.container():

            st.subheader("📈 Live Telemetry")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "CPU %",
                f"{t.cpu_percent:.1f}"
            )

            c2.metric(
                "Memory %",
                f"{t.memory_percent:.1f}"
            )

            c3.metric(
                "Latency",
                f"{t.latency_ms:.0f} ms"
            )

            c4.metric(
                "HTTP 500",
                t.http_500_errors
            )

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "DB Latency",
                f"{t.db_latency_ms:.0f} ms"
            )

            c2.metric(
                "Connections",
                t.active_connections
            )

            c3.metric(
                "Pods",
                t.pod_count
            )

            c4.metric(
                "Restarts",
                t.restart_count
            )

            cpu = min(t.cpu_percent / 100.0, 1.0)

            mem = min(t.memory_percent / 100.0, 1.0)

            st.write("CPU Utilization")

            st.progress(cpu)

            st.write("Memory Utilization")

            st.progress(mem)

    # ---------------------------------------------------------
    # Workflow Progress
    # ---------------------------------------------------------

    def render_workflow_deprecated(self, state: WorkflowState):
        with self.workflow_placeholder.container():
            st.subheader("⚙ Workflow")

            stages = list(WorkflowStage)
            cols = st.columns(len(stages))
            for col, stage in zip(cols, stages):
                if stage.value < state.current_stage.value:
                    col.success(f"✅\n\n{stage.name}")

                elif stage == state.current_stage:
                    col.warning(f"▶\n\n{stage.name}")

                else:
                    col.info(f"○\n\n{stage.name}")


    def render_workflow(self, state: WorkflowState):    
        with self.workflow_placeholder.container():
            st.subheader("⚙ Workflow")

            stages = list(WorkflowStage)
            cols = st.columns(len(stages))
            current_index = stages.index(state.current_stage)

            for i, (col, stage) in enumerate(zip(cols, stages)):
                if i < current_index:
                    col.success(f"✅\n\n{stage.name}")
                elif i == current_index:
                    col.warning(f"▶\n\n{stage.name}")
                else:
                    col.info(f"○\n\n{stage.name}")
        # ---------------------------------------------------------
    # Details Section
    # ---------------------------------------------------------

    def render_details(self, state: WorkflowState):

        with self.details_placeholder.container():

            tabs = st.tabs(
                [
                    "📚 RAG",
                    "🧠 RCA",
                    "🎯 PPO",
                    "⚡ Execution",
                    "🏆 Reward",
                    "✅ Resolution",
                    "🖥 Console",
                    "🔄 Pipeline"
                ]
            )

            with tabs[0]:
                self.render_rag(state)

            with tabs[1]:
                self.render_rca(state)

            with tabs[2]:
                self.render_ppo(state)

            with tabs[3]:
                self.render_execution(state)

            with tabs[4]:
                self.render_reward(state)

            with tabs[5]:
                self.render_resolution(state)

            with tabs[6]:
                self.render_console(state)

            with tabs[7]:
                self.render_pipeline(state)

    # ---------------------------------------------------------
    # RAG
    # ---------------------------------------------------------

    def render_rag(self, state: WorkflowState):

        if not state.retrieved_incidents:
            st.info("Waiting for RAG retrieval...")
            return

        result = state.retrieved_incidents
        doc = result["document"]

        df = pd.DataFrame([
            {
                "Incident": doc["incident"],
                "Similarity": round(result["score"], 3),
                "Root Cause": doc["root_cause"],
                "Resolution": doc["recommended_action"],
            }
        ])

        st.dataframe(df, use_container_width=True, hide_index=True,)

    # ---------------------------------------------------------
    # RCA
    # ---------------------------------------------------------

    def render_rca(self, state: WorkflowState):

        if not state.rca_result:
            st.info("Waiting for RCA...")
            return

        rca = state.rca_result

        st.metric("Predicted Root Cause", rca["root_cause"])
        st.progress(float(rca["confidence"]))
        st.caption(f"Incident: {rca['incident']}")
        st.metric("Recommended Action", rca["recommended_action"])

    # ---------------------------------------------------------
    # PPO
    # ---------------------------------------------------------

    def render_ppo(self, state: WorkflowState):

        if not state.ppo_result:
            st.info("Waiting for PPO prediction...")
            return

        ppo = state.ppo_result

        st.metric("Selected Action", ppo["action_name"])
        st.metric("Action ID", ppo["action"])
        st.caption("Prediction generated by trained PPO model.")

    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    def render_execution(self, state: WorkflowState):

        if state.execution_result is None:
            st.info("Waiting for execution...")
            return

        execution = state.execution_result

        before = execution.before_metrics
        after = execution.after_metrics

        metrics = [
            (
                "CPU %",
                before.cpu_percent,
                after.cpu_percent,
            ),
            (
                "Memory %",
                before.memory_percent,
                after.memory_percent,
            ),
            (
                "Latency",
                before.latency_ms,
                after.latency_ms,
            ),
            (
                "DB Latency",
                before.db_latency_ms,
                after.db_latency_ms,
            ),
            (
                "HTTP500",
                before.http_500_errors,
                after.http_500_errors,
            ),
        ]

        rows = []

        for name, b, a in metrics:

            rows.append(
                {
                    "Metric": name,
                    "Before": b,
                    "After": a,
                }
            )

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.metric("Execution Time", f"{execution.execution_time_seconds:.1f} sec",)

        if execution.success:
            st.success("Autonomous action successfully mitigated the incident.")
        else:
            st.error("Autonomous action failed.")

    # ---------------------------------------------------------
    # Reward
    # ---------------------------------------------------------

    def render_reward(self, state):

        if state.reward_result is None:
            st.info("Waiting for reward...")
            return

        reward = state.reward_result

        c1, c2 = st.columns(2)
        c3, c4 = st.columns(2)

        c1.metric(
            "Structured Reward",
            f"{reward.structured_reward:.2f}",
        )

        c2.metric(
            "LLM Reward",
            f"{reward.llm_reward:.2f}",
        )

        c3.metric(
            "Adaptive Alpha",
            f"{reward.adaptive_alpha:.3f}",
        )

        c4.metric(
            "Hybrid Reward",
            f"{reward.final_reward:.2f}",
        )

        st.metric("Episode Reward", f"{state.environment_reward:.2f}",)

        import pandas as pd
        rows = []
        for reward in state.reward_history:
            rows.append(
                {
                    "Step": reward["step"],
                    "Action": reward["action"],
                    "Structured": round(reward["structured_reward"],2),
                    "LLM": (
                        "Not Evaluated"
                        if reward["llm_reward"] is None
                        else round(reward["llm_reward"],2)
                    ),
                    "α": (
                        "Not Evaluated"
                        if reward["adaptive_alpha"] is None
                        else round(reward["adaptive_alpha"],3)
                    ),
                    "Hybrid": round(reward["hybrid_reward"],2),
                }
            )

        df = pd.DataFrame(rows)

        st.markdown("### Episode Reward Breakdown")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            """
    Hybrid reward is returned from the AIOps Environment.
            """
        )

    # ---------------------------------------------------------
    # Resolution
    # ---------------------------------------------------------

    def render_resolution(self, state: WorkflowState):

        if state.resolution_result is None:
            st.info("Incident not resolved yet.")
            return

        resolution = state.resolution_result

        if resolution.resolved:
            st.success("✅ Incident Resolved")
        else:
            st.error("Incident Unresolved")

        st.metric("MTTR", f"{resolution.mttr_seconds:.1f} sec",)
        st.metric("Confidence", f"{resolution.confidence * 100:.1f}%", )

        # st.write(resolution.summary)
        st.markdown("### Resolution Summary")
        st.code(resolution.summary, language="text")

    # ---------------------------------------------------------
    # Logs
    # ---------------------------------------------------------

    def render_logs(self, state: WorkflowState):

        with self.logs_placeholder.container():

            st.subheader("📜 Workflow Logs")

            if not state.logs:
                st.info("No logs available.")
                return

            lines = []

            for log in state.logs:

                lines.append(
                    f"[{log.timestamp:%H:%M:%S}] "
                    f"[{log.stage}] "
                    f"{log.message}"
                )

            st.code(
                "\n".join(lines),
                language="text",
            )

    def render_console(self, state: WorkflowState):
        if not state.console_logs:
            st.info("No console messages.")
            return

        st.code("\n".join(state.console_logs), language="text")

    def render_pipeline(self,state):
        retrieved = "-"
        root_cause = "-"
        action = "-"
        reward = "-"

        if state.retrieved_incidents:
            retrieved = state.retrieved_incidents["document"]["incident"]

        if state.rca_result:
            root_cause = state.rca_result["root_cause"]

        if state.ppo_result:
            action = state.ppo_result["action_name"]

        if state.reward_result:
            reward = f"{state.reward_result.final_reward:.2f}"
        elif state.environment_reward:
            reward = f"{state.environment_reward:.2f}"

        st.subheader("Pipeline Status")

        st.write("✅ Telemetry")

        if state.retrieved_incidents:
            st.write("✅ Hybrid RAG")
            st.write(f"• {retrieved}")
        else:
            st.write("⏳ Hybrid RAG")

        if state.rca_result:
            st.write("✅ RCA")
            st.write(f"• {root_cause}")
        else:
            st.write("⏳ RCA")

        if state.state_vector:
            st.write("✅ State Builder")
        else:
            st.write("⏳ State Builder")

        if state.ppo_result:
            st.write("✅ PPO")
            st.write(f"• {action}")
        else:
            st.write("⏳ PPO")

        if state.execution_result:
            st.write("✅ Execution")
        else:
            st.write("⏳ Execution")

        if state.reward_result:
            st.write("✅ Reward")
        else:
            st.write("⏳ Reward")

        if state.resolution_result:
            st.write("✅ Resolution")
        else:
            st.write("⏳ Resolution")