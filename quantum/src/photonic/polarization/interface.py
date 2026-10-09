"""Polarization control interface."""
from __future__ import annotations
from abc import ABC, abstractmethod

class PolarizationController(ABC):
    @abstractmethod
    def set_angle(self, angle_deg: float) -> None: ...
    @abstractmethod
    def get_angle(self) -> float: ...
    @abstractmethod
    def compensate_drift(self, measured_visibility: float) -> float: ...
