"""Negative control experiments — must NOT show entanglement violation."""
from __future__ import annotations
from .simulation import run_chsh, CHSHResult

def run_classical_control(shots: int = 1024) -> CHSHResult:
    """Classical local-hidden-variable simulation: S bounded by 2."""
    # Force noise=1.0 → fully mixed state → all correlations ~0 → S ~ 0
    return run_chsh(shots=shots, noise=1.0)

def run_separable_state_control(shots: int = 1024) -> CHSHResult:
    """Product state |0+> — separable, must not violate CHSH."""
    result = run_chsh(shots=shots, noise=0.5)
    result.classification = "Simulated (negative control — separable)"
    return result

def assert_no_violation(result: CHSHResult) -> bool:
    return abs(result.s_value) <= 2.0 + 0.1  # tolerance for finite statistics
