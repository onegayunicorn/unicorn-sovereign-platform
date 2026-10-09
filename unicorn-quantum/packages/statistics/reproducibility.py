"""Reproducibility manifest — pins everything needed to reproduce a result."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Optional
import json, hashlib

@dataclass
class ReproducibilityManifest:
    job_id: str
    circuit_checksum: str
    backend: str
    backend_version: str
    shots: int
    seed: Optional[int]
    compiler_version: str
    transpilation_report_hash: str
    dependency_lockfile_hash: str
    result_hash: str
    classification: str = "Simulated"

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2)

    @property
    def manifest_hash(self) -> str:
        return hashlib.sha256(self.to_json().encode()).hexdigest()
