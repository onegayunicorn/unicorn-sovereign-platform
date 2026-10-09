"""OpenQASM 2 parser — produces UnicornCircuitIR."""
from __future__ import annotations
import re
from ...circuit_ir.models import UnicornCircuitIR, IROp

GATE_MAP = {"h": "h", "x": "x", "y": "y", "z": "z", "cx": "cx", "cz": "cz",
            "swap": "swap", "rx": "rx", "ry": "ry", "rz": "rz"}

def parse_qasm2(source: str) -> UnicornCircuitIR:
    num_qubits = 0; num_clbits = 0; ops = []
    for line in source.splitlines():
        line = line.strip().rstrip(";")
        if not line or line.startswith("//") or line.startswith("OPENQASM") or line.startswith("include"):
            continue
        m = re.match(r"qreg\s+(\w+)\[(\d+)\]", line)
        if m: num_qubits = int(m.group(2)); continue
        m = re.match(r"creg\s+(\w+)\[(\d+)\]", line)
        if m: num_clbits = int(m.group(2)); continue
        m = re.match(r"measure\s+(\w+)\[(\d+)\]\s*->\s*(\w+)\[(\d+)\]", line)
        if m:
            ops.append(IROp(op="measure", qubits=[int(m.group(2))], params=[float(m.group(4))])); continue
        m = re.match(r"(\w+)\s*(?:\(([^)]+)\))?\s+(.+)", line)
        if m and m.group(1) in GATE_MAP:
            gate = GATE_MAP[m.group(1)]
            params = [float(p) for p in m.group(2).split(",")] if m.group(2) else []
            qubits = [int(re.search(r"\[(\d+)\]", q).group(1)) for q in m.group(3).split(",")]
            ops.append(IROp(op=gate, qubits=qubits, params=params))
    return UnicornCircuitIR(num_qubits=num_qubits, num_clbits=num_clbits, operations=ops)
