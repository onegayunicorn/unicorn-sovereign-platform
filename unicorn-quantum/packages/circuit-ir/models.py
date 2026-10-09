"""UnicornCircuitIR — canonical intermediate representation."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class IROp(BaseModel):
    op: str
    qubits: List[int]
    params: List[float] = Field(default_factory=list)
    condition: Optional[dict] = None

class UnicornCircuitIR(BaseModel):
    """Canonical IR — single source of truth between QASM, compiler, and execution."""
    ir_version: Literal["1.0"] = "1.0"
    num_qubits: int
    num_clbits: int = 0
    operations: List[IROp] = Field(default_factory=list)
    global_phase: float = 0.0
    metadata: dict = Field(default_factory=dict)

    def semantic_hash(self) -> str:
        import hashlib
        # Semantic hash ignores metadata and global phase for equivalence checks
        core = {"nq": self.num_qubits, "nc": self.num_clbits,
                "ops": [(o.op, tuple(o.qubits), tuple(o.params)) for o in self.operations]}
        return hashlib.sha256(repr(core).encode()).hexdigest()
