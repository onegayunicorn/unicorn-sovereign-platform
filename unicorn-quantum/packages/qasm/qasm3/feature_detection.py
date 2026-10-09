"""Feature capability matrix — which QASM3 features each backend supports."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set

@dataclass
class BackendCapabilities:
    backend: str
    supported_features: Set[str] = field(default_factory=set)
    max_qubits: int = 0
    max_shots: int = 100000

CAPABILITY_MATRIX: Dict[str, BackendCapabilities] = {
    "simulator_statevector": BackendCapabilities(
        "simulator_statevector",
        {"qasm2", "qasm3_basic", "mid_circuit_measurement", "parametric_gates"},
        max_qubits=32),
    "ibm_kyiv": BackendCapabilities(
        "ibm_kyiv", {"qasm2", "dynamic_circuits"}, max_qubits=127, max_shots=100000),
}

def detect_features(source: str) -> Set[str]:
    features = set()
    if "OPENQASM 3" in source: features.add("qasm3")
    if "while" in source or "for" in source: features.add("control_flow")
    if "reset" in source: features.add("mid_circuit_reset")
    return features

def backend_supports(backend: str, features: Set[str]) -> bool:
    caps = CAPABILITY_MATRIX.get(backend)
    if not caps: return False
    return features.issubset(caps.supported_features) or "qasm2" in caps.supported_features
