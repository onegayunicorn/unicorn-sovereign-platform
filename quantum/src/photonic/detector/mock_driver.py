"""Mock detector driver — no hardware required."""
from __future__ import annotations
import random, time
from .interface import PhotonDetector, DetectorMetrics

class MockDetector(PhotonDetector):
    def __init__(self, channel: int = 0):
        self.channel = channel
        self._armed = False
        self._timestamps: list[int] = []

    def arm(self) -> None:
        self._armed = True

    def disarm(self) -> None:
        self._armed = False

    def get_metrics(self) -> DetectorMetrics:
        return DetectorMetrics(
            efficiency=random.uniform(0.4, 0.7),
            dark_count_rate_hz=random.uniform(50, 500),
            dead_time_ns=random.uniform(20, 50),
            timing_jitter_ps=random.uniform(50, 200),
            afterpulsing_prob=random.uniform(0.001, 0.01),
        )

    def read_timestamps(self) -> list[int]:
        if not self._armed:
            return []
        n = random.randint(0, 10)
        base = time.time_ns()
        return [base + random.randint(0, 1_000_000) for _ in range(n)]
