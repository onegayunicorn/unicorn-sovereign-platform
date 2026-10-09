"""GHZ state test."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages"))
from circuit_ir.builder import IRBuilder
from providers.simulator.statevector import StateVectorSimulator

def test_ghz_3_qubits():
    b = IRBuilder(3, 3).h(0).cx(0,1).cx(1,2)
    for q in range(3): b.measure(q, q)
    sim = StateVectorSimulator()
    counts = sim.sample(b.build(), shots=1024)
    total = sum(counts.values())
    p000 = counts.get("000", 0) / total
    p111 = counts.get("111", 0) / total
    assert p000 + p111 > 0.90, f"GHZ corrupted: p000={p000}, p111={p111}"
