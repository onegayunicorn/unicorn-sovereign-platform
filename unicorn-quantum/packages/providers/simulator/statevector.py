"""CPU state-vector simulator."""
from __future__ import annotations
import numpy as np, random
from typing import Dict
from ...circuit_ir.models import UnicornCircuitIR

class StateVectorSimulator:
    """Minimal state-vector simulator supporting h, x, cx, measure."""

    def __init__(self):
        self.name = "statevector_simulator"

    def available(self) -> bool:
        return True

    def sample(self, circuit: UnicornCircuitIR, shots: int = 1024) -> Dict[str, int]:
        n = circuit.num_qubits
        state = np.zeros(2**n, dtype=complex)
        state[0] = 1.0
        for op in circuit.operations:
            if op.op == "measure":
                continue  # handled at end
            elif op.op == "h":
                self._apply_h(state, n, op.qubits[0])
            elif op.op == "x":
                self._apply_x(state, n, op.qubits[0])
            elif op.op == "cx":
                self._apply_cx(state, n, op.qubits[0], op.qubits[1])
        probs = np.abs(state) ** 2
        probs = probs / probs.sum()
        outcomes = [format(i, f"0{n}b") for i in range(2**n)]
        counts: Dict[str, int] = {}
        for _ in range(shots):
            o = random.choices(outcomes, weights=probs)[0]
            counts[o] = counts.get(o, 0) + 1
        return counts

    def _apply_h(self, state, n, q):
        for i in range(0, 2**n, 2**(q+1)):
            for j in range(2**q):
                a, b = state[i+j], state[i+j+2**q]
                state[i+j] = (a + b) / np.sqrt(2)
                state[i+j+2**q] = (a - b) / np.sqrt(2)

    def _apply_x(self, state, n, q):
        for i in range(0, 2**n, 2**(q+1)):
            for j in range(2**q):
                state[i+j], state[i+j+2**q] = state[i+j+2**q], state[i+j]

    def _apply_cx(self, state, n, ctrl, tgt):
        for i in range(2**n):
            if (i >> ctrl) & 1 and not (i >> tgt) & 1:
                j = i | (1 << tgt)
                state[i], state[j] = state[j], state[i]
