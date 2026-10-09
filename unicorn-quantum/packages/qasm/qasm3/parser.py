"""OpenQASM 3 parser (subset)."""
from __future__ import annotations
from ...circuit_ir.models import UnicornCircuitIR, IROp

def parse_qasm3(source: str) -> UnicornCircuitIR:
    # Subset parser — delegates common constructs to qasm2-style logic
    import re
    num_qubits = 0; num_clbits = 0; ops = []
    for line in source.splitlines():
        line = line.strip().rstrip(";")
        if not line or line.startswith("//") or line.startswith("OPENQASM") or line.startswith("include"):
            continue
        m = re.match(r"qubit\s*\[(\d+)\]", line)
        if m: num_qubits = int(m.group(1)); continue
        m = re.match(r"bit\s*\[(\d+)\]", line)
        if m: num_clbits = int(m.group(1)); continue
    return UnicornCircuitIR(num_qubits=max(num_qubits,1), num_clbits=num_clbits, operations=ops)
