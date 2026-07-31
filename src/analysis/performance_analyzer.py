import json
import os

import pandas as pd
import matplotlib.pyplot as plt

PIPELINE_COMPONENTS = [
    "telemetry_latency_ms",
    "rag_latency_ms",
    "rca_latency_ms",
    "state_builder_latency_ms",
    "llm_latency_ms",
]

class PerformanceAnalyzer:
    def __init__(
        self,
        performance_file="results/performance_report.json",
        evaluation_file="results/evaluation_summary.json",
        output_dir="results/performance"
    ):

        self.output_dir = output_dir

        os.makedirs(output_dir, exist_ok=True)

        with open(performance_file, "r") as f:
            self.performance = json.load(f)

        with open(evaluation_file, "r") as f:
            self.evaluation = json.load(f)
        
    ########################################################

    def latency_dataframe(self):
        rows = []

        for metric, values in self.performance.items():
            if not isinstance(values, dict):
                continue

            if "average" not in values:
                continue

            rows.append({
                "Component": metric,
                "Average(ms)": values["average"],
                "Minimum(ms)": values["minimum"],
                "Maximum(ms)": values["maximum"]
            })

        df = pd.DataFrame(rows)
        return df

    ########################################################
    def throughput(self):
        episode_latency = self.performance["episode_latency_ms"]["average"]

        episodes_per_second = round(1000 / episode_latency,3)
        incidents_per_hour = round(episodes_per_second * 3600, 2)

        incidents_per_day = round(incidents_per_hour * 24,2)

        return {
            "episodes_per_second": episodes_per_second,
            "incidents_per_hour": incidents_per_hour,
            "incidents_per_day": incidents_per_day
        }

    ########################################################
    def component_percentage(self):
        """
        Compute contribution of each component
        to one decision pipeline.
        """
        pipeline = self.performance["pipeline_latency_ms"]["average"]

        components = {
            "Telemetry": self.performance["telemetry_latency_ms"]["average"],
            "RAG": self.performance["rag_latency_ms"]["average"],
            "RCA": self.performance["rca_latency_ms"]["average"],
            "State Builder": self.performance["state_builder_latency_ms"]["average"],
            "PPO": self.performance["ppo_inference_ms"]["average"]
        }

        rows = []
        total_known = 0

        # Add all known components first
        for name, latency in components.items():
            total_known += latency
            rows.append({
                "Component": name,
                "Average(ms)": round(latency, 3),
                "Percentage": round((latency / pipeline) * 100, 2)
            })

        # Add remaining environment processing ONCE
        remaining = pipeline - total_known

        rows.append({
            "Component": "Environment Processing",
            "Average(ms)": round(remaining, 3),
            "Percentage": round((remaining / pipeline) * 100, 2)
        })

        # Add pipeline total ONCE
        rows.append({
            "Component": "Decision Pipeline Total",
            "Average(ms)": round(pipeline, 3),
            "Percentage": 100.0
        })

        return pd.DataFrame(rows)

    ########################################################
    def scalability_summary(self):
        tp = self.throughput()
        return {
            "Decision Pipeline (ms)": self.performance["pipeline_latency_ms"]["average"],
            "Episode Latency (ms)": self.performance["episode_latency_ms"]["average"],
            "Episodes/sec": tp["episodes_per_second"],
            "Incidents/hour": tp["incidents_per_hour"],
            "Incidents/day": tp["incidents_per_day"],
            "CPU (%)": self.performance["cpu_percent"]["average"],
            "Memory (MB)": self.performance["memory_mb"]["average"]
        }

    ########################################################
    def operational_summary(self):
        return {
            "Episodes": self.evaluation["episodes"],
            "Success Rate": self.evaluation["success_rate"],
            "Average Reward": self.evaluation["avg_reward"],
            "Recommendation Follow Rate": self.evaluation["recommendation_follow_rate"],
            "MTTR": self.evaluation["mttr_minutes"],
            "Average Steps": self.evaluation["avg_steps"]
        }
    
    ########################################################
    def save_tables(self):
        latency = self.latency_dataframe()
        latency.to_csv(os.path.join(self.output_dir, "latency_breakdown.csv"),index=False)
        latency.to_excel(os.path.join(self.output_dir, "latency_breakdown.xlsx"), index=False)
        ##########################################
        percentages = self.component_percentage()
        percentages.to_csv(os.path.join(self.output_dir,"component_percentage.csv"),index=False)
        percentages.to_excel(os.path.join(self.output_dir,"component_percentage.xlsx"),index=False)
        ##########################################        
        #scalability = self.scalability_summary()
        scalability = pd.DataFrame([self.scalability_summary()])
        scalability.to_csv(os.path.join(self.output_dir,"scalability_summary.csv"),index=False)
        scalability.to_excel(os.path.join(self.output_dir,"scalability_summary.xlsx"), index=False)
        ##########################################
        operational = pd.DataFrame([self.operational_summary()])
        operational.to_csv(os.path.join(self.output_dir,"operational_summary.csv"),index=False)
        operational.to_excel(os.path.join(self.output_dir,"operational_summary.xlsx"), index=False)

    ########################################################

    def latency_plot(self):
        latency_metrics = [
            "telemetry_latency_ms",
            "rag_latency_ms",
            "rca_latency_ms",
            "state_builder_latency_ms",
            "ppo_inference_ms",
            "pipeline_latency_ms"
        ]

        df = self.latency_dataframe()
        df = df[df["Component"].isin(latency_metrics)]

        plt.figure(figsize=(10,5))
        plt.bar(df["Component"], df["Average(ms)"])

        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Average Latency (ms)")

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir,"latency_bar_chart.png"))

        plt.close()

    ########################################################

    def percentage_plot(self):
        df = self.component_percentage()
        if df is None:
            return

        plt.figure(figsize=(8,5))
        plt.bar(df["Component"],df["Percentage"])

        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Percentage of Pipeline")

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir,"component_percentage.png"))

        plt.close()

    ########################################################

    def cpu_memory_plot(self):

        cpu = self.performance["cpu_percent"]["average"]
        mem = self.performance["memory_mb"]["average"]

        plt.figure(figsize=(6,4))
        plt.bar(["CPU %", "Memory MB"], [cpu, mem])

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir,"cpu_memory_usage.png"))

        plt.close()

    ########################################################

    def summary(self):
        throughput = self.throughput()
        percentages = self.component_percentage()
        
        report = []
        report.append("# Performance Analysis")
        report.append("")

        report.append("## Computational Performance")
        report.append("")
        report.append(self.component_percentage().to_markdown(index=False))
        report.append("")
        report.append(
            f"Average Decision Pipeline Latency: "
            f"{self.performance['pipeline_latency_ms']['average']:.2f} ms"
        )
        report.append("")
        
        report.append("## Scalability")
        scale = self.scalability_summary()
        for key, value in scale.items():
            report.append(f"- {key}: {value}")
        report.append("")

        report.append("## Operational Performance")
        operational = self.operational_summary()
        for key, value in operational.items():
            report.append(f"- {key}: {value}")
        report.append("")

        report.append("## Resource Usage")
        report.append(f"- CPU: {self.performance['cpu_percent']['average']:.2f}%")
        report.append(f"- Memory: {self.performance['memory_mb']['average']:.2f} MB")

        with open(os.path.join(self.output_dir,"performance_report.md"),"w",encoding="utf-8") as f:
            f.write("\n".join(report))

    ########################################################
    def generate(self):
        self.save_tables()
        self.latency_plot()
        self.percentage_plot()
        self.cpu_memory_plot()
        self.summary()

        print("Performance analysis completed.")