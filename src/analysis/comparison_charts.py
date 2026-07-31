import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

class ComparisonCharts:

    def __init__(self, tables):

        self.tables = tables

        self.output_dir = tables.output_dir

        self.figsize = (10, 6)

        self.dpi = 300

    def save_bar_chart(
        self,
        dataframe,
        x,
        y,
        title,
        ylabel,
        filename
    ):

        ax = dataframe.plot(
            x=x,
            y=y,
            kind="bar",
            figsize=self.figsize,
            rot=0
        )

        ax.set_title(title, fontsize=14)

        ax.set_ylabel(ylabel)

        ax.grid(axis="y", alpha=0.3)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.2f",
                fontsize=9
            )

        plt.tight_layout()

        plt.savefig(
            self.output_dir / filename,
            dpi=self.dpi
        )

        plt.close()

    def operational_charts(self):

        df = self.tables.operational_dataframe()

        metrics = [

            ("Average Reward", "Reward", "avg_reward.png"),

            ("Success Rate", "Rate", "success_rate.png"),

            ("Recommendation Follow Rate",
            "Rate",
            "follow_rate.png"),

            ("MTTR (minutes)",
            "Minutes",
            "mttr.png"),

            ("Average Steps",
            "Steps",
            "avg_steps.png")
        ]

        for metric, ylabel, file in metrics:

            row = df[df["Metric"] == metric]

            chart = row.drop(columns=["Metric"]).T

            chart.columns = [metric]

            chart = chart.reset_index()

            chart.columns = ["Experiment", metric]

            self.save_bar_chart(

                chart,

                "Experiment",

                [metric],

                metric,

                ylabel,

                file
            )

    def action_distribution_chart(self):

        df = self.tables.action_distribution_dataframe()

        ax = df.plot(

            x="Action",

            kind="bar",

            figsize=self.figsize,

            rot=0
        )

        ax.set_title(
            "Action Distribution"
        )

        ax.set_ylabel("Count")

        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()

        plt.savefig(
            self.output_dir /
            "action_distribution.png",
            dpi=self.dpi
        )

        plt.close()

    def successful_actions_chart(self):
        df = self.tables.successful_actions_dataframe()
        ax = df.plot(
            x="Successful Action",
            kind="bar",
            figsize=self.figsize,
            rot=0
        )
        ax.set_title("Successful Action Distribution")
        ax.set_ylabel("Count")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / "successful_actions.png", dpi=self.dpi)
        plt.close()

    def incident_dataframe_chart(self):
        df = self.tables.incident_dataframe()
        ax = df.plot(
            x="Incident",
            kind="bar",
            figsize=self.figsize,
            rot=0
        )
        ax.set_title("Incident Distribution")
        ax.set_ylabel("Count")
        ax.grid(axis="y", alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / "incident_distribution.png", dpi=self.dpi)
        plt.close()

    def success_by_incident_chart(self):
        """
        Compare incident resolution success
        between Fixed Alpha and Adaptive Alpha.
        """

        df = self.tables.success_by_incident_dataframe()

        if df.empty:
            print("No success-by-incident data found.")
            return

        # Structured doesn't contain this metric.
        columns = [
            c for c in df.columns
            if c in ["Fixed Alpha", "Adaptive Alpha"]
        ]

        ax = df.plot(
            x="Incident",
            y=columns,
            kind="bar",
            figsize=self.figsize,
            rot=20
        )

        ax.set_title(
            "Success Rate by Incident Type",
            fontsize=14
        )

        ax.set_ylabel("Success Rate")

        ax.grid(axis="y", alpha=0.3)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.2f",
                fontsize=8
            )

        plt.tight_layout()

        plt.savefig(
            self.output_dir /
            "success_by_incident.png",
            dpi=self.dpi
        )

        plt.close()


    def performance_metric_chart(
        self,
        metric_name,
        file_name,
        ylabel
    ):
        """
        Generate a single performance chart.
        """

        df = self.tables.performance_dataframe()

        row = df[df["Metric"] == metric_name]

        if row.empty:
            return

        chart = row[["Average", "Minimum", "Maximum"]].T

        chart.columns = [metric_name]

        chart = chart.reset_index()

        chart.columns = ["Statistic", metric_name]

        ax = chart.plot(
            x="Statistic",
            y=[metric_name],
            kind="bar",
            figsize=self.figsize,
            rot=0
        )

        ax.set_title(metric_name)

        ax.set_ylabel(ylabel)

        ax.grid(axis="y", alpha=0.3)

        for container in ax.containers:
            ax.bar_label(
                container,
                fmt="%.2f",
                fontsize=8
            )

        plt.tight_layout()

        plt.savefig(
            self.output_dir / file_name,
            dpi=self.dpi
        )

        plt.close()
        

    def performance_charts(self):
        """
        Generate adaptive performance charts.
        """

        metrics = [

            (
                "ppo_inference_ms",
                "ppo_latency.png",
                "Milliseconds"
            ),

            (
                "pipeline_latency_ms",
                "pipeline_latency.png",
                "Milliseconds"
            ),

            (
                "llm_latency_ms",
                "llm_latency.png",
                "Milliseconds"
            ),

            (
                "cpu_percent",
                "cpu_usage.png",
                "CPU (%)"
            ),

            (
                "memory_mb",
                "memory_usage.png",
                "Memory (MB)"
            ),

            (
                "episode_latency_ms",
                "episode_latency.png",
                "Milliseconds"
            ),

            (
                "rag_latency_ms",
                "rag_latency.png",
                "Milliseconds"
            ),

            (
                "rca_latency_ms",
                "rca_latency.png",
                "Milliseconds"
            ),

            (
                "telemetry_latency_ms",
                "telemetry_latency.png",
                "Milliseconds"
            ),

            (
                "state_builder_latency_ms",
                "state_builder_latency.png",
                "Milliseconds"
            )
        ]

        for metric, file_name, ylabel in metrics:

            self.performance_metric_chart(
                metric,
                file_name,
                ylabel
            )

    def generate(self):

        print()

        print("=" * 60)
        print("Generating comparison charts...")
        print("=" * 60)

        self.operational_charts()

        self.action_distribution_chart()

        self.successful_actions_chart()

        self.incident_dataframe_chart()

        self.success_by_incident_chart()

        self.performance_charts()

        print()

        print("Charts generated successfully.")

        print("=" * 60)