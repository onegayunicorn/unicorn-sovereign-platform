"""Bell/CHSH state simulation — Stage 0 software-only validation."""
from __future__ import annotations
import math, random
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class CHSHResult:
    s_value: float
    correlation_terms: List[float]
    shots: int
    classification: str = "Simulated"

def bell_state_counts(shots: int = 1024, noise: float = 0.0) -> Dict[str, int]:
    """Simulate |Phi+> = (|00>+|11>)/sqrt2 measurement counts with depolarizing noise."""
    counts = {"00": 0, "01": 0, "10": 0, "11": 0}
    p_correct = (1.0 - noise) * 0.5
    p_error = noise * 0.25
    probs = {
        "00": p_correct + p_error,
        "11": p_correct + p_error,
        "01": p_error,
        "10": p_error,
    }
    total = sum(probs.values())
    probs = {k: v/total for k, v in probs.items()}
    keys = list(probs.keys())
    weights = [probs[k] for k in keys]
    for _ in range(shots):
        outcome = random.choices(keys, weights=weights)[0]
        counts[outcome] += 1
    return counts

def chsh_correlation(a: int, b: int, shots: int = 1024, noise: float = 0.0) -> float:
    """E(a,b) = P(same) - P(different) for measurement settings a,b.
    Quantum: E = -cos(2*(a-b)). With noise: scaled by (1-noise)."""
    theta = 2 * (a - b) * math.pi / 180.0
    ideal = -math.cos(theta)
    return ideal * (1.0 - noise)

def run_chsh(shots: int = 1024, noise: float = 0.0) -> CHSHResult:
    """CHSH: S = E(a,b) - E(a,b') + E(a',b) + E(a',b'), with a=0, a'=45, b=22.5, b'=67.5 degrees.
    Classical bound |S| <= 2; quantum max = 2*sqrt(2) ~ 2.828."""
    settings = [(0, 22.5), (0, 67.5), (45, 22.5), (45, 67.5)]
    terms = [chsh_correlation(a, b, shots, noise) for a, b in settings]
    s = terms[0] - terms[1] + terms[2] + terms[3]
    return CHSHResult(s_value=s, correlation_terms=terms, shots=shots,
                      classification="Simulated")
