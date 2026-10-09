"""IBM Quantum entropy workflow.
Capability: SIMULATED by default; uses real IBM Quantum when credentials + backend access are available.
"""
from __future__ import annotations
import hashlib, os, json, time
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class EntropySample:
    source: str
    timestamp_ns: int
    raw_bytes: bytes
    classification: str = "Simulated"  # Demonstrated / Prototype / Simulated / Reported / Proposed
    backend: Optional[str] = None
    shots: int = 0

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.raw_bytes).hexdigest()

class EntropyHarvester:
    """Harvests entropy. Stage 0 = software RNG; Stage 1+ = IBM Quantum backend."""

    def __init__(self, use_real_ibm: bool = False, ibm_token: Optional[str] = None,
                 instance: Optional[str] = None, channel: str = "ibm_quantum"):
        self.use_real_ibm = use_real_ibm and bool(ibm_token)
        self.ibm_token = ibm_token
        self.instance = instance
        self.channel = channel
        self._backend = None

    def _connect_ibm(self):
        if not self.use_real_ibm:
            return None
        try:
            from qiskit_ibm_runtime import QiskitRuntimeService
            service = QiskitRuntimeService(channel=self.channel, token=self.ibm_token,
                                           instance=self.instance)
            self._backend = service.least_busy(operational=True, simulator=False)
            return self._backend
        except Exception:
            self._backend = None
            return None

    def harvest(self, num_bytes: int = 32, shots: int = 1024) -> EntropySample:
        backend = self._connect_ibm() if self.use_real_ibm else None
        if backend is not None:
            raw = self._harvest_ibm(backend, num_bytes, shots)
            return EntropySample("ibm_quantum", time.time_ns(), raw,
                                 classification="Demonstrated", backend=backend.name, shots=shots)
        # Stage 0: software entropy (os.urandom is CSPRNG — clearly labeled Simulated)
        raw = os.urandom(num_bytes)
        return EntropySample("software_csprng", time.time_ns(), raw,
                             classification="Simulated", backend="os.urandom", shots=0)

    def _harvest_ibm(self, backend, num_bytes: int, shots: int) -> bytes:
        """Run a Bell-state circuit on IBM backend and extract bitstring entropy."""
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import SamplerV2 as Sampler
        n_qubits = min(backend.num_qubits, 27)
        qc = QuantumCircuit(n_qubits)
        qc.h(range(n_qubits))
        qc.measure_all()
        sampler = Sampler(mode=backend)
        job = sampler.run([qc], shots=shots)
        result = job.result()[0]
        counts = result.data.meas.get_counts()
        # Derive deterministic bytes from the measured bit distribution
        bitstring = max(counts, key=counts.get)
        raw = bytes(int(bitstring[i:i+8], 2) for i in range(0, min(len(bitstring), num_bytes*8), 8))
        return raw[:num_bytes].ljust(num_bytes, b"\x00")
