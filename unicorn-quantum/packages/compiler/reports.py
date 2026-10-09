"""Compilation reports."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List
import json, hashlib, time

@dataclass
class CompilationReport:
    job_id: str
    circuit_checksum: str
    backend: str
    original_depth: int
    transpiled_depth: int
    original_gate_count: int
    transpiled_gate_count: int
    basis_gates: List[str]
    timestamp: float
    compiler_version: str = "1.0.0"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @property
    def report_hash(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()
