"""Photonic source abstract interface.
Candidate designs: heralded SPDC, entangled-pair source, integrated photonic source, certified commercial source.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class SourceConfig:
    pump_power_mw: float
    temperature_c: float
    polarization: str
    coincidence_window_ns: float
    spectral_filter_nm: float

@dataclass
class SourceMetrics:
    pair_rate_hz: float
    heralding_efficiency: float
    visibility: float
    drift_ppm_per_hour: float

class PhotonicSource(ABC):
    @abstractmethod
    def initialize(self, config: SourceConfig) -> None: ...
    @abstractmethod
    def start(self) -> None: ...
    @abstractmethod
    def stop(self) -> None: ...
    @abstractmethod
    def get_metrics(self) -> SourceMetrics: ...
    @abstractmethod
    def set_polarization(self, angle_deg: float) -> None: ...
    @abstractmethod
    def health_check(self) -> bool: ...
    @abstractmethod
    def shutdown_safe(self) -> None: ...
