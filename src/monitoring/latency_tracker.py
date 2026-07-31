"""
Latency tracking utilities.

Measures execution time of individual pipeline components.
"""

from __future__ import annotations

import time
from contextlib import ContextDecorator


class LatencyTracker(ContextDecorator):
    """
    Context manager to measure elapsed time.

    Example:
        with LatencyTracker("rag") as timer:
            rag.retrieve(query)

        print(timer.elapsed_ms)
    """

    def __init__(self, component: str):
        self.component = component
        self.start = None
        self.end = None
        self.elapsed_ms = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        self.end = time.perf_counter()
        self.elapsed_ms = (self.end - self.start) * 1000.0
        return False