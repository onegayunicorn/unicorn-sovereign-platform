"""
Python validation test — runs on every commit
pytest schemas/tests/validate-python.py -v
"""
import json
import sys
from pathlib import Path

# Make the schemas package importable when running pytest from repo root
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT.parent))  # repo root, so `schemas.models.python` resolves

from schemas.models.python import QuantumJob, QuantumCircuit, Artifact, AuditEvent
from schemas.models.python.validators import validate_against_schema

FIXTURES = ROOT / "fixtures"


def test_job_fixture_pydantic():
    with open(FIXTURES / "job.bell-state.json") as f:
        data = json.load(f)
    job = QuantumJob.model_validate(data)
    assert job.jobId == "8f54979c-b4cf-46ad-bd39-34896e320001"
    assert job.correlationId == "sovereign-bell-0001"
    assert job.status == "approved"


def test_circuit_fixture_pydantic():
    with open(FIXTURES / "circuit.bell-state.json") as f:
        data = json.load(f)
    circuit = QuantumCircuit.model_validate(data)
    assert circuit.circuitId == "bell-state-v1"
    assert circuit.format == "openqasm3"
    assert circuit.qubitCount == 2


def test_artifact_fixture_pydantic():
    with open(FIXTURES / "artifact.result.json") as f:
        data = json.load(f)
    artifact = Artifact.model_validate(data)
    assert artifact.artifactType == "result"
    assert artifact.encrypted is True


def test_audit_lifecycle_pydantic():
    with open(FIXTURES / "audit-event.lifecycle.json") as f:
        events = json.load(f)
    ids = set()
    job_ids = set()
    for e in events:
        event = AuditEvent.model_validate(e)
        ids.add(event.correlationId)
        job_ids.add(event.jobId)
        assert event.eventId is not None
    assert len(ids) == 1, "All events must share one correlationId"
    assert len(job_ids) == 1, "All events must share one jobId"


def test_job_json_schema():
    with open(FIXTURES / "job.bell-state.json") as f:
        data = json.load(f)
    ok, msg = validate_against_schema(data, "job")
    assert ok, msg
