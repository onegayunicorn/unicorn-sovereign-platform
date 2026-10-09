"""Evidence bundle generator.
Required manifest fields (all required):
experiment_id, node_ids, source_format, circuit_checksum, backend, shots,
classification (Demonstrated/Prototype/Simulated/Reported/Proposed),
result_artifact_uri, independent_review_status
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum
from .hashing import sha256_obj

class Classification(str, Enum):
    DEMONSTRATED = "Demonstrated"
    PROTOTYPE = "Prototype"
    SIMULATED = "Simulated"
    REPORTED = "Reported"
    PROPOSED = "Proposed"

class ReviewStatus(str, Enum):
    NOT_REVIEWED = "not_reviewed"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    CONDITIONAL = "conditional"

REQUIRED_FIELDS = [
    "experiment_id", "node_ids", "source_format", "circuit_checksum",
    "backend", "shots", "classification", "result_artifact_uri",
    "independent_review_status",
]

@dataclass
class EvidenceManifest:
    experiment_id: str
    node_ids: List[str]
    source_format: str
    circuit_checksum: str
    backend: str
    shots: int
    classification: Classification
    result_artifact_uri: str
    independent_review_status: ReviewStatus
    # Optional but recommended
    calibration_records_uri: Optional[str] = None
    raw_data_uri: Optional[str] = None
    analysis_code_version: Optional[str] = None
    dependency_lockfile: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        d["classification"] = self.classification.value
        d["independent_review_status"] = self.independent_review_status.value
        return d

    def manifest_hash(self) -> str:
        return sha256_obj(self.to_dict())

    def validate_required(self) -> List[str]:
        d = self.to_dict()
        missing = [f for f in REQUIRED_FIELDS if not d.get(f)]
        return missing
