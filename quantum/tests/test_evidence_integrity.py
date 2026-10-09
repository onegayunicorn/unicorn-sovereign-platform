"""Evidence chain tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from evidence.hashing import HashChain, sha256_obj
from evidence.manifest import EvidenceManifest, Classification, ReviewStatus
from evidence.validation import validate_manifest

def test_hash_chain_linkage():
    chain = HashChain()
    e1 = chain.append({"a": 1})
    e2 = chain.append({"b": 2})
    assert e2["prev_hash"] == e1["entry_hash"]
    assert chain.root_hash == e2["entry_hash"]

def test_manifest_validation_simulated():
    m = EvidenceManifest(
        experiment_id="exp-001", node_ids=["node-1"],
        source_format="qasm2", circuit_checksum="abc123",
        backend="simulator", shots=1024,
        classification=Classification.SIMULATED,
        result_artifact_uri="s3://bucket/result.json",
        independent_review_status=ReviewStatus.NOT_REVIEWED,
    )
    v = validate_manifest(m)
    assert v.publishable  # Simulated doesn't require review
    assert v.missing_fields == []

def test_manifest_demonstrated_requires_review():
    m = EvidenceManifest(
        experiment_id="exp-002", node_ids=["node-1"],
        source_format="qasm2", circuit_checksum="def456",
        backend="ibm_kyiv", shots=1024,
        classification=Classification.DEMONSTRATED,
        result_artifact_uri="s3://bucket/result2.json",
        independent_review_status=ReviewStatus.NOT_REVIEWED,
    )
    v = validate_manifest(m)
    assert not v.review_gate_passed
    assert not v.publishable
