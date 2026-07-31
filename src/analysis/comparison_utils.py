"""
Common utility functions for experiment comparison.
"""

from pathlib import Path
from typing import Dict


def ensure_directory(path: Path):
    """
    Create directory if it doesn't exist.
    """
    path.mkdir(parents=True, exist_ok=True)


def percent(value):
    """
    Convert decimal values into percentages.

    Example:
        0.581 -> 58.10
    """
    if value is None:
        return None
    return round(value * 100, 2)


def get_nested(dictionary: Dict, keys, default=None):
    """
    Safely read nested dictionary values.

    Example:
        get_nested(data,
                   ["performance",
                    "pipeline_latency_ms",
                    "average"])
    """
    current = dictionary

    for key in keys:
        if not isinstance(current, dict):
            return default

        current = current.get(key)

        if current is None:
            return default

    return current


def flatten_metric(metric):
    """
    Extract metric value.

    Supports:
        123
        {"average":123}
    """

    if isinstance(metric, dict):

        if "average" in metric:
            return metric["average"]

    return metric