"""IR builder — fluent construction of UnicornCircuitIR."""
from __future__ import annotations
from .models import UnicornCircuitIR, IROp

class IRBuilder:
    def __init__(self, num_qubits: int, num_clbits: int = 0):
        self._ir = UnicornCircuitIR(num_qubits=num_qubits, num_clbits=num_clbits)

    def h(self, q: int) -> "IRBuilder":
        self._ir.operations.append(IROp(op="h", qubits=[q])); return self

    def cx(self, q0: int, q1: int) -> "IRBuilder":
        self._ir.operations.append(IROp(op="cx", qubits=[q0, q1])); return self

    def measure(self, q: int, c: int) -> "IRBuilder":
        self._ir.operations.append(IROp(op="measure", qubits=[q], params=[float(c)])); return self

    def build(self) -> UnicornCircuitIR:
        return self._ir

    @staticmethod
    def bell_state() -> UnicornCircuitIR:
        return IRBuilder(2, 2).h(0).cx(0, 1).measure(0, 0).measure(1, 1).build()
