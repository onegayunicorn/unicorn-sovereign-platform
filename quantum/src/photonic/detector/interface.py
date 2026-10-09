"""Detector abstract interface. SPAD / SNSPD classes."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class DetectorMetrics:
    efficiency: float
    dark_count_rate_hz: float
    dead_time_ns: float
    timing_jitter_ps: float
    afterpulsing_prob: float

class PhotonDetector(ABC):
    @abstractmethod
    def arm(self) -> None: ...
    @abstractmethod
    def disarm(self) -> None: ...
    @abstractmethod
    def get_metrics(self) -> DetectorMetrics: ...
    @abstractmethod
    def read_timestamps(self) -> list[int]: ...
