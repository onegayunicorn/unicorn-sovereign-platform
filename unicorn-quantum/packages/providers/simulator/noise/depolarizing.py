"""Depolarizing noise model."""
from __future__ import annotations
import random
from typing import Dict

class DepolarizingNoise:
    """Applies depolarizing noise to measurement counts: with probability p,
    a random bit-flip occurs on each qubit independently."""
    def __init__(self, error_prob: float = 0.01):
        self.error_prob = error_prob

    def apply(self, counts: Dict[str, int], num_qubits: int) -> Dict[str, int]:
        noisy: Dict[str, int] = {}
        for bitstring, count in counts.items():
            for _ in range(count):
                bits = list(bitstring)
                for q in range(num_qubits):
                    if random.random() < self.error_prob:
                        bits[q] = "1" if bits[q] == "0" else "0"
                o = "".join(bits)
                noisy[o] = noisy.get(o, 0) + 1
        return noisy
