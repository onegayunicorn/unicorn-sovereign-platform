"""Mock photonic source driver — no hardware required. Stage 0."""
from __future__ import annotations
import time, random
from .interface import PhotonicSource, SourceConfig, SourceMetrics

class MockPhotonicSource(PhotonicSource):
    def __init__(self):
        self._running = False
        self._config: SourceConfig | None = None
        self._pol_angle = 0.0

    def initialize(self, config: SourceConfig) -> None:
        self._config = config
        self._pol_angle = 0.0

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def get_metrics(self) -> SourceMetrics:
        return SourceMetrics(
            pair_rate_hz=random.uniform(1e5, 5e5),
            heralding_efficiency=random.uniform(0.3, 0.6),
            visibility=random.uniform(0.92, 0.98),
            drift_ppm_per_hour=random.uniform(1, 10),
        )

    def set_polarization(self, angle_deg: float) -> None:
        self._pol_angle = angle_deg

    def health_check(self) -> bool:
        return self._config is not None

    def shutdown_safe(self) -> None:
        self._running = False
