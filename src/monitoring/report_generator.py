"""
Performance report generation.
"""
from pathlib import Path
import json

class ReportGenerator:
    @staticmethod
    def save(metrics_summary, filename="results/performance_report.json"):
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            json.dump(metrics_summary, f, indent=4)

        print(f"\nPerformance report saved to {filename}")