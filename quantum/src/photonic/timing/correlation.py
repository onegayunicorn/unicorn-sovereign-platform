"""Timestamp correlation logic — coincidence window matching."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class CoincidenceResult:
    coincidences: int
    accidentals: int
    singles_a: int
    singles_b: int
    window_ns: float

def correlate(timestamps_a: List[int], timestamps_b: List[int],
              window_ns: float = 2.0) -> CoincidenceResult:
    """Two-sided coincidence matching within window_ns."""
    coincidences = 0
    used_b = set()
    for ta in timestamps_a:
        for j, tb in enumerate(timestamps_b):
            if j in used_b:
                continue
            if abs(ta - tb) <= window_ns * 1000:  # ns → ps
                coincidences += 1
                used_b.add(j)
                break
    accidentals = max(0, min(len(timestamps_a), len(timestamps_b)) - coincidences)
    return CoincidenceResult(coincidences, accidentals,
                             len(timestamps_a), len(timestamps_b), window_ns)
