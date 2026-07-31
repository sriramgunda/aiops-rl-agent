"""
demo_app.py

Main Streamlit application for the Autonomous AI SRE Demo.
"""

from __future__ import annotations

import time
import streamlit as st

from demo_engine import DemoEngine
from ui_renderer import UIRenderer
from scenario_repository import (
    SCENARIOS,
    get_scenario,
)
from workflow_state import Severity


# -------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------

def render_sidebar():

    st.sidebar.title("⚙ Demo Configuration")

    scenario_name = st.sidebar.selectbox(
        "Incident Scenario",
        list(SCENARIOS.keys()),
    )

    severity = st.sidebar.selectbox(
        "Severity",
        [
            Severity.CRITICAL,
            Severity.HIGH,
            Severity.MEDIUM,
            Severity.LOW,
        ],
        format_func=lambda x: x.name,
    )

    delay = st.sidebar.slider(
        "Workflow Delay (sec)",
        0.0,
        3.0,
        0.8,
        0.1,
    )

    auto_scroll = st.sidebar.checkbox(
        "Auto Refresh",
        value=True,
    )

    run_demo = st.sidebar.button(
        "▶ Run Autonomous Resolution",
        type="primary",
        use_container_width=True,
    )

    return (
        scenario_name,
        severity,
        delay,
        auto_scroll,
        run_demo,
    )


# -------------------------------------------------------------
# Main
# -------------------------------------------------------------

def main():

    renderer = UIRenderer()

    renderer.initialize()

    (
        scenario_name,
        severity,
        delay,
        auto_refresh,
        run_demo,
    ) = render_sidebar()

    st.sidebar.markdown("---")

    st.sidebar.info(
        """
        Demo Pipeline

        Incident

        ↓

        Telemetry

        ↓

        Hybrid RAG

        ↓

        RCA

        ↓

        State Builder
        
        ↓

        PPO

        ↓

        Action Execution

        ↓

        Reward Evaluation

        ↓

        Resolution
        """
    )

    if not run_demo:

        st.info(
            "Select a scenario from the left and click **Run Autonomous Resolution**."
        )

        return

    scenario = get_scenario(scenario_name)

    engine = DemoEngine()

    progress = st.progress(0)

    status = st.empty()

    estimated_steps = 5

    total_steps = (
        5      # telemetry..ppo
        + estimated_steps
        + 2    # reward + resolution
    )

    current = 0

    for stage, state in engine.execute(
        scenario=scenario,
        severity=severity,
        delay=0,
    ):

        current += 1

        value = min(current / total_steps, 1.0)
        progress.progress(value)

        status.info(f"Current Stage : {stage.name}")

        renderer.render_dashboard(state)

        if auto_refresh:
            time.sleep(delay)

    progress.progress(1.0)

    status.success("✔ Autonomous Resolution Completed")

    st.balloons()


# -------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------

if __name__ == "__main__":
    main()