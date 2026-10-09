"""Statistical analysis + confidence intervals for Bell/CHSH results."""
from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List

@dataclass
class ConfidenceInterval:
    estimate: float
    lower: float
    upper: float
    confidence: float = 0.95

def wald_interval(p_hat: float, n: int, z: float = 1.96) -> ConfidenceInterval:
    se = math.sqrt(p_hat * (1 - p_hat) / n) if 0 < p_hat < 1 else 0.0
    return ConfidenceInterval(p_hat, max(0.0, p_hat - z*se), min(1.0, p_hat + z*se))

def chsh_confidence_interval(s_value: float, shots: int, z: float = 1.96) -> ConfidenceInterval:
    """Approximate CI for CHSH S-value. Each term has variance ~1/shots; S is sum of 4 terms."""
    se = 2.0 * math.sqrt(4.0 / shots)  # conservative bound
    return ConfidenceInterval(s_value, s_value - z*se, s_value + z*se)

def violates_classical_bound(ci: ConfidenceInterval) -> bool:
    """True if the 95% CI lower bound exceeds the classical bound of 2."""
    return ci.lower > 2.0
