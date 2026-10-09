"""Result normalization — counts → probabilities with confidence intervals."""
from __future__ import annotations
import math
from typing import Dict, Tuple

def normalize_counts(counts: Dict[str, int]) -> Dict[str, float]:
    total = sum(counts.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in counts.items()}

def binomial_ci(p: float, n: int, z: float = 1.96) -> Tuple[float, float]:
    se = math.sqrt(p * (1 - p) / n) if 0 < p < 1 else 0.0
    return (max(0.0, p - z*se), min(1.0, p + z*se))
