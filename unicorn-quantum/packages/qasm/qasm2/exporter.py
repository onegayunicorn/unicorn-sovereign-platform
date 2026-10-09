"""OpenQASM 2 exporter — from UnicornCircuitIR."""
from __future__ import annotations
from ...circuit_ir.models import UnicornCircuitIR

def export_qasm2(ir: UnicornCircuitIR) -> str:
    lines = ["OPENQASM 2.0;", 'include "qelib1.inc";',
             f"qreg q[{ir.num_qubits}];"]
    if ir.num_clbits > 0:
        lines.append(f"creg c[{ir.num_clbits}];")
    for op in ir.operations:
        if op.op == "measure":
            c = int(op.params[0]) if op.params else 0
            lines.append(f"measure q[{op.qubits[0]}] -> c[{c}];")
        elif op.params:
            params = ",".join(str(p) for p in op.params)
            qs = ",".join(f"q[{q}]" for q in op.qubits)
            lines.append(f"{op.op}({params}) {qs};")
        else:
            qs = ",".join(f"q[{q}]" for q in op.qubits)
            lines.append(f"{op.op} {qs};")
    return "\n".join(lines) + "\n"
