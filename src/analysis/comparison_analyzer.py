"""
Experiment Comparison Analyzer

Compares:

1. Structured Reward
2. Fixed Hybrid Reward
3. Adaptive Hybrid Reward
"""

from pathlib import Path

from comparison_loader import ComparisonLoader
from comparison_utils import ensure_directory
from comparison_tables import ComparisonTables
from comparison_charts import ComparisonCharts
from comparison_report import ComparisonReport

class ComparisonAnalyzer:

    def __init__(
        self,
        experiment_dir="results/experiments",
        output_dir="results/comparison"
    ):

        self.experiment_dir = Path(experiment_dir)

        self.output_dir = Path(output_dir)

        ensure_directory(self.output_dir)

        self.loader = ComparisonLoader(
            self.experiment_dir
        )

        self.experiments = self.loader.load()

        self.structured = self.experiments["structured"]

        self.fixed = self.experiments["fixed_alpha"]

        self.adaptive = self.experiments["adaptive_alpha"]

    ##########################################################

    def summary(self):

        print()

        print("=" * 70)

        print("Loaded Experiments")

        print("=" * 70)

        for name, experiment in self.experiments.items():

            print()

            print(name)

            print("-" * 30)

            print(
                f"Episodes : "
                f"{experiment['episodes']}"
            )

            print(
                f"Reward   : "
                f"{experiment['avg_reward']}"
            )

            print(
                f"Success  : "
                f"{experiment['success_rate']}"
            )

            print(
                f"MTTR     : "
                f"{experiment['mttr_minutes']}"
            )

    ##########################################################

    def compare_metrics(self):

        """
        Returns
        -------

        Dictionary used by all
        tables/charts/reports.
        """

        metrics = {

            "Average Reward": {

                "Structured":
                    self.structured["avg_reward"],

                "Fixed Alpha":
                    self.fixed["avg_reward"],

                "Adaptive Alpha":
                    self.adaptive["avg_reward"]

            },

            "Success Rate": {

                "Structured":
                    self.structured["success_rate"],

                "Fixed Alpha":
                    self.fixed["success_rate"],

                "Adaptive Alpha":
                    self.adaptive["success_rate"]

            },

            "Recommendation Follow Rate": {

                "Structured":
                    self.structured[
                        "recommendation_follow_rate"
                    ],

                "Fixed Alpha":
                    self.fixed[
                        "recommendation_follow_rate"
                    ],

                "Adaptive Alpha":
                    self.adaptive[
                        "recommendation_follow_rate"
                    ]
            },

            "MTTR (minutes)": {

                "Structured":
                    self.structured[
                        "mttr_minutes"
                    ],

                "Fixed Alpha":
                    self.fixed[
                        "mttr_minutes"
                    ],

                "Adaptive Alpha":
                    self.adaptive[
                        "mttr_minutes"
                    ]
            },

            "Average Steps": {

                "Structured":
                    self.structured[
                        "avg_steps"
                    ],

                "Fixed Alpha":
                    self.fixed[
                        "avg_steps"
                    ],

                "Adaptive Alpha":
                    self.adaptive[
                        "avg_steps"
                    ]
            }

        }

        return metrics

    ##########################################################

    def compare_actions(self):

        return {

            "Structured":
                self.structured[
                    "action_distribution"
                ],

            "Fixed Alpha":
                self.fixed[
                    "action_distribution"
                ],

            "Adaptive Alpha":
                self.adaptive[
                    "action_distribution"
                ]
        }

    ##########################################################

    def compare_successful_actions(self):

        return {

            "Structured":
                self.structured[
                    "successful_action_distribution"
                ],

            "Fixed Alpha":
                self.fixed[
                    "successful_action_distribution"
                ],

            "Adaptive Alpha":
                self.adaptive[
                    "successful_action_distribution"
                ]
        }

    ##########################################################

    def compare_incidents(self):

        return {

            "Structured":
                self.structured[
                    "incident_types"
                ],

            "Fixed Alpha":
                self.fixed[
                    "incident_types"
                ],

            "Adaptive Alpha":
                self.adaptive[
                    "incident_types"
                ]
        }

    ##########################################################

    def adaptive_performance(self):

        return self.adaptive.get(
            "performance",
            {}
        )


if __name__ == "__main__":

    analyzer = ComparisonAnalyzer()
    analyzer.summary()

    metrics = analyzer.compare_metrics()
    print()

    print(metrics)

    tables = ComparisonTables(analyzer)
    tables.generate()

    charts = ComparisonCharts(tables)
    charts.generate()

    report = ComparisonReport(analyzer, tables)
    report.generate()