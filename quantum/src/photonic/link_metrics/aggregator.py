"""CAR, visibility, drift, uptime aggregation for photonic links."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import time

@dataclass
class LinkMetrics:
    link_id: str
    car: float
    visibility: float
    drift_ppm: float
    uptime_fraction: float
    data_loss_fraction: float
    timestamp: float = field(default_factory=time.time)

class LinkMetricsAggregator:
    def __init__(self, link_id: str):
        self.link_id = link_id
        self._history: List[LinkMetrics] = []

    def record(self, car: float, visibility: float, drift_ppm: float,
               uptime: float, data_loss: float) -> None:
        self._history.append(LinkMetrics(self.link_id, car, visibility, drift_ppm, uptime, data_loss))

    def latest(self) -> LinkMetrics | None:
        return self._history[-1] if self._history else None

    def average_visibility(self) -> float:
        if not self._history:
            return 0.0
        return sum(m.visibility for m in self._history) / len(self._history)
