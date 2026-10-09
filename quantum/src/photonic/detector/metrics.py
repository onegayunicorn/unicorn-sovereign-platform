"""Dark count, jitter, efficiency metrics computation."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .interface import DetectorMetrics

@dataclass
class DetectorCharacterization:
    detector_id: str
    metrics: DetectorMetrics
    coincidence_rate_hz: float
    accidental_coincidence_rate_hz: float
    car: float  # coincidence-to-accidental ratio
    basis_dependent_loss: float

def compute_car(coincidence: float, accidental: float) -> float:
    return coincidence / accidental if accidental > 0 else float("inf")

def characterize_detector(detector_id: str, m: DetectorMetrics,
                          coincidence_rate: float, accidental_rate: float,
                          basis_loss: float) -> DetectorCharacterization:
    return DetectorCharacterization(
        detector_id=detector_id, metrics=m,
        coincidence_rate_hz=coincidence_rate,
        accidental_coincidence_rate_hz=accidental_rate,
        car=compute_car(coincidence_rate, accidental_rate),
        basis_dependent_loss=basis_loss,
    )
