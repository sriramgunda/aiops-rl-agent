"""
Resource monitoring.

Collects CPU and Memory statistics.
"""

from __future__ import annotations

import os
import psutil


class ResourceMonitor:
    def __init__(self):
        self.process = psutil.Process(os.getpid())

    def snapshot(self):
        """
        Returns current resource utilization.
        """
        return {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "memory_mb": self.process.memory_info().rss / (1024 ** 2)
        }