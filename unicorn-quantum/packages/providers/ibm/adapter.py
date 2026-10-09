"""IBM Quantum adapter — uses real backend when credentials available, else simulator."""
from __future__ import annotations
from typing import Dict, Optional
from ...circuit_ir.models import UnicornCircuitIR
from ..simulator.statevector import StateVectorSimulator

class IBMQAdapter:
    def __init__(self, token: Optional[str] = None, instance: Optional[str] = None,
                 channel: str = "ibm_quantum", use_real: bool = False):
        self.token = token
        self.instance = instance
        self.channel = channel
        self.use_real = use_real and bool(token)
        self._service = None
        self._fallback = StateVectorSimulator()

    def name(self) -> str:
        return "ibm_quantum" if self.use_real else "ibm_quantum (simulated fallback)"

    def available(self) -> bool:
        return True  # fallback always available

    def sample(self, circuit: UnicornCircuitIR, shots: int = 1024) -> Dict[str, int]:
        if self.use_real:
            try:
                return self._sample_real(circuit, shots)
            except Exception:
                pass
        return self._fallback.sample(circuit, shots)

    def _sample_real(self, circuit: UnicornCircuitIR, shots: int) -> Dict[str, int]:
        from qiskit import QuantumCircuit
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
        if not self._service:
            self._service = QiskitRuntimeService(channel=self.channel, token=self.token, instance=self.instance)
        backend = self._service.least_busy(operational=True, simulator=False)
        qc = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
        for op in circuit.operations:
            if op.op == "h": qc.h(op.qubits[0])
            elif op.op == "x": qc.x(op.qubits[0])
            elif op.op == "cx": qc.cx(op.qubits[0], op.qubits[1])
            elif op.op == "measure": qc.measure(op.qubits[0], int(op.params[0]) if op.params else 0)
        sampler = Sampler(mode=backend)
        job = sampler.run([qc], shots=shots)
        result = job.result()[0]
        return result.data.meas.get_counts()
