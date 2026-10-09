"""Circuit Pydantic model."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class GateType(str, Enum):
    H = "h"; X = "x"; Y = "y"; Z = "z"
    CX = "cx"; CZ = "cz"; SWAP = "swap"
    RX = "rx"; RY = "ry"; RZ = "rz"
    MEASURE = "measure"; BARRIER = "barrier"

class GateOp(BaseModel):
    gate: GateType
    qubits: List[int]
    parameter: Optional[float] = None

class CircuitModel(BaseModel):
    circuit_id: str
    num_qubits: int = Field(ge=1, le=1000)
    operations: List[GateOp] = Field(default_factory=list)
    classical_bits: int = 0
    metadata: dict = Field(default_factory=dict)

    def checksum(self) -> str:
        import hashlib
        canonical = self.model_dump_json(sort_keys=True)
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]
