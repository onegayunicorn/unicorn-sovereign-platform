"""Experiment scheduler — source activation, calibration windows, basis settings, detector acquisition, link tests, maintenance, cross-node experiments."""
from __future__ import annotations
import heapq, time
from dataclasses import dataclass, field
from typing import Callable, List

@dataclass(order=True)
class ScheduledJob:
    scheduled_at: float
    priority: int
    job_id: str
    experiment_id: str = field(compare=False)
    node_ids: List[str] = field(default_factory=list, compare=False)

class ExperimentScheduler:
    def __init__(self):
        self._queue: list[ScheduledJob] = []

    def schedule(self, job: ScheduledJob) -> None:
        heapq.heappush(self._queue, job)

    def due_jobs(self, now: float | None = None) -> List[ScheduledJob]:
        now = now or time.time()
        due = []
        while self._queue and self._queue[0].scheduled_at <= now:
            due.append(heapq.heappop(self._queue))
        return due
