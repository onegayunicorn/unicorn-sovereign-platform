"""ISA transpilation pipeline — maps IR to backend-specific instruction set."""
from __future__ import annotations
from ..circuit_ir.models import UnicornCircuitIR, IROp
from dataclasses import dataclass

@dataclass
class TranspilationReport:
    original_op_count: int
    transpiled_op_count: int
    gates_decomposed: list[str]
    depth: int

def transpile(ir: UnicornCircuitIR, backend_isa: str = "universal") -> tuple[UnicornCircuitIR, TranspilationReport]:
    # Simple transpilation: ensure basis gates {cx, rz, sx, x} for IBM-like ISA
    decomposed = []
    gates = set()
    for op in ir.operations:
        gates.add(op.op)
        if op.op in ("h",) and backend_isa == "ibm":
            # h = rz(pi/2) sx rz(pi/2)
            decomposed.append(IROp(op="rz", qubits=op.qubits, params=[1.57079632679]))
            decomposed.append(IROp(op="sx", qubits=op.qubits))
            decomposed.append(IROp(op="rz", qubits=op.qubits, params=[1.57079632679]))
        else:
            decomposed.append(op)
    transpiled = UnicornCircuitIR(num_qubits=ir.num_qubits, num_clbits=ir.num_clbits, operations=decomposed)
    report = TranspilationReport(len(ir.operations), len(decomposed), list(gates), len(decomposed))
    return transpiled, report
