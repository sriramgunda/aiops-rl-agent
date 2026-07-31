"""
Loads evaluation summaries from experiments.
"""

import json
from pathlib import Path


class ComparisonLoader:

    def __init__(self, experiment_directory):

        self.base_path = Path(experiment_directory)

        self.required = [
            "structured",
            "fixed_alpha",
            "adaptive_alpha"
        ]

    def load_json(self, file):

        with open(file, "r", encoding="utf8") as f:
            return json.load(f)

    def validate(self):

        missing = []

        for experiment in self.required:

            file = (
                self.base_path /
                experiment /
                "evaluation_summary.json"
            )

            if not file.exists():
                missing.append(str(file))

        if missing:

            raise FileNotFoundError(
                "\n".join(missing)
            )

    def load(self):

        self.validate()

        experiments = {}

        for experiment in self.required:

            file = (
                self.base_path /
                experiment /
                "evaluation_summary.json"
            )

            experiments[experiment] = self.load_json(file)

        return experiments