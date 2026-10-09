"""Noise channel models for Bell experiments."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class NoiseModel(str, Enum):
    DEPOLARIZING = "depolarizing"
    AMPLITUDE_DAMPING = "amplitude_damping"
    PHASE_DAMPING = "phase_damping"
    BIT_FLIP = "bit_flip"
    PHASE_FLIP = "phase_flip"

@dataclass
class NoiseChannel:
    model: NoiseModel
    parameter: float  # error probability / rate
    channel: str = "both"  # alice, bob, both

    def effective_visibility(self) -> float:
        if self.model == NoiseModel.DEPOLARIZING:
            return 1.0 - self.parameter
        if self.model == NoiseModel.AMPLITUDE_DAMPING:
            return 1.0 - self.parameter / 2.0
        if self.model == NoiseModel.PHASE_DAMPING:
            return 1.0 - self.parameter
        if self.model == NoiseModel.BIT_FLIP:
            return 1.0 - 2 * self.parameter
        if self.model == NoiseModel.PHASE_FLIP:
            return 1.0 - 2 * self.parameter
        return 1.0
