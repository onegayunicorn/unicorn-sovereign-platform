"""Sampler + Estimator protocols."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Protocol
from ..circuit_ir.models import UnicornCircuitIR

class Sampler(Protocol):
    def run(self, circuits: list[UnicornCircuitIR], shots: int) -> list[Dict[str, int]]: ...

class Estimator(Protocol):
    def estimate(self, circuit: UnicornCircuitIR, observable: list[float]) -> float: ...

class BackendProvider(ABC):
    @abstractmethod
    def name(self) -> str: ...
    @abstractmethod
    def sample(self, circuit: UnicornCircuitIR, shots: int) -> Dict[str, int]: ...
    @abstractmethod
    def available(self) -> bool: ...
