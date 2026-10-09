"""Bell state acceptance test: ~50% |00> / ~50% |11> with 1024 shots."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages"))
from circuit_ir.builder import IRBuilder
from providers.simulator.statevector import StateVectorSimulator

def test_bell_state_50_50():
    ir = IRBuilder.bell_state()
    sim = StateVectorSimulator()
    counts = sim.sample(ir, shots=1024)
    total = sum(counts.values())
    p00 = counts.get("00", 0) / total
    p11 = counts.get("11", 0) / total
    assert 0.40 < p00 < 0.60, f"p00={p00}"
    assert 0.40 < p11 < 0.60, f"p11={p11}"
    assert p00 + p11 > 0.90, "too much noise in Bell state"
