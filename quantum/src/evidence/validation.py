"""Completeness + review gate logic."""
from __future__ import annotations
from .manifest import EvidenceManifest, Classification, ReviewStatus
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationResult:
    manifest_hash: str
    missing_fields: List[str]
    classification_ok: bool
    review_gate_passed: bool
    publishable: bool

def validate_manifest(m: EvidenceManifest) -> ValidationResult:
    missing = m.validate_required()
    classification_ok = isinstance(m.classification, Classification)
    # Review gate: Demonstrated results require independent review before publication
    review_gate_passed = True
    if m.classification == Classification.DEMONSTRATED:
        review_gate_passed = m.independent_review_status in (ReviewStatus.PASSED, ReviewStatus.CONDITIONAL)
    publishable = len(missing) == 0 and classification_ok and review_gate_passed
    return ValidationResult(
        manifest_hash=m.manifest_hash(),
        missing_fields=missing,
        classification_ok=classification_ok,
        review_gate_passed=review_gate_passed,
        publishable=publishable,
    )
