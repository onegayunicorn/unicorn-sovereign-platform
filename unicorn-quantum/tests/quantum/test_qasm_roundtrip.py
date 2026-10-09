"""OpenQASM 2 round-trip: import → IR → export → re-parse → semantic equivalence."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages"))
from qasm.qasm2.parser import parse_qasm2
from qasm.qasm2.exporter import export_qasm2

BELL_QASM = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];
h q[0];
cx q[0],q[1];
measure q[0] -> c[0];
measure q[1] -> c[1];
"""

def test_qasm2_roundtrip():
    ir1 = parse_qasm2(BELL_QASM)
    qasm = export_qasm2(ir1)
    ir2 = parse_qasm2(qasm)
    assert ir1.semantic_hash() == ir2.semantic_hash()
