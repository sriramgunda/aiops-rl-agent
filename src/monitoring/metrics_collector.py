"""
Central metrics collector.

All pipeline components push metrics here.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean


class MetricsCollector:
    def __init__(self):
        self.metrics = defaultdict(list)

    def add_metric(self, name: str, value):
        self.metrics[name].append(value)

    def add_metrics(self, metrics: dict):
        for key, value in metrics.items():
            self.add_metric(key, value)

    def get_average(self, name):
        values = self.metrics.get(name, [])
        if not values:
            return 0
        return mean(values)

    def summary(self):
        output = {}
        for key, values in self.metrics.items():
            output[key] = {
                "count": len(values),
                "average": round(mean(values), 3),
                "minimum": round(min(values), 3),
                "maximum": round(max(values), 3)
            }

        return output

    def clear(self):
        self.metrics.clear()
    
    