"""Fail-closed tests for the read-only Platform capability endpoint."""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
PLATFORM_ROOT = REPO_ROOT / "unicorn-quantum"
sys.path.insert(0, str(PLATFORM_ROOT))

from apps.api.main import app  # noqa: E402
from apps.api.api.v1 import capabilities  # noqa: E402

client = TestClient(app)
NOW = datetime(2026, 10, 11, 12, 0, tzinfo=timezone.utc)
REVISION = "a" * 40


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    monkeypatch.delenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", raising=False)
    monkeypatch.delenv("SOVEREIGN_SOURCE_REVISION", raising=False)


def write_evidence(tmp_path, records):
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(records), encoding="utf-8")
    return str(path)


def evidence_record(capability_id, *, status="HEALTHY", classification="VALIDATED",
                    observed_at=None, source_revision=REVISION, evidence_uri="test://evidence"):
    return {
        "capability_id": capability_id,
        "status": status,
        "classification": classification,
        "observed_at": observed_at or "2026-10-11T11:59:00Z",
        "source_revision": source_revision,
        "evidence_uri": evidence_uri,
        "freshness_seconds": 300,
    }


def test_endpoint_is_read_only_and_defaults_unknown():
    response = client.get("/api/v1/capabilities/")
    assert response.status_code == 200
    report = response.json()
    assert report["status"] == "UNKNOWN"
    assert report["source"] == "unicorn-sovereign-platform"
    # No per-capability claim is emitted without an immutable source revision.
    assert report["capabilities"] == []
    assert report["registered_capability_count"] == len(capabilities.REGISTRY)
    assert report["reason"] == "source_revision_unavailable"
    assert client.post("/api/v1/capabilities/").status_code == 405
    assert client.put("/api/v1/capabilities/").status_code == 405
    assert client.delete("/api/v1/capabilities/").status_code == 405


def test_current_revision_linked_evidence_can_report_healthy(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    records = [
        evidence_record(entry["capability_id"])
        for entry in capabilities.REGISTRY
    ]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    monkeypatch.setattr(capabilities, "_registered_module_available", lambda _module: True)
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "HEALTHY"
    assert all(event["payload"]["status"] == "HEALTHY" for event in report["capabilities"])
    assert all(event["provenance"]["revision"] == REVISION for event in report["capabilities"])
    assert all(event["classification"] == "VALIDATED" for event in report["capabilities"])


def test_missing_revision_fails_closed(tmp_path, monkeypatch):
    records = [evidence_record(entry["capability_id"]) for entry in capabilities.REGISTRY]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "UNKNOWN"
    assert report["capabilities"] == []
    assert report["reason"] == "source_revision_unavailable"


def test_stale_evidence_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    old = (NOW - timedelta(minutes=20)).isoformat().replace("+00:00", "Z")
    records = [evidence_record(entry["capability_id"], observed_at=old) for entry in capabilities.REGISTRY]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "UNKNOWN"
    assert all("stale" in event["payload"]["reason"] for event in report["capabilities"])


def test_revision_mismatch_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    records = [evidence_record(entry["capability_id"], source_revision="b" * 40) for entry in capabilities.REGISTRY]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "UNKNOWN"


def test_malformed_evidence_fails_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    path = tmp_path / "bad.json"
    path.write_text("{not json", encoding="utf-8")
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", str(path))
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "UNKNOWN"
    assert all(event["payload"]["reason"] == "evidence_source_unreadable" for event in report["capabilities"])


def test_unavailable_module_never_reports_healthy(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    records = [evidence_record(entry["capability_id"]) for entry in capabilities.REGISTRY]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    monkeypatch.setattr(capabilities, "_registered_module_available", lambda _module: False)
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "UNKNOWN"
    assert all(event["payload"]["status"] == "UNKNOWN" for event in report["capabilities"])


def test_simulator_evidence_label_is_not_promoted(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    records = [
        evidence_record(entry["capability_id"], classification="MEASURED")
        for entry in capabilities.REGISTRY
    ]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    monkeypatch.setattr(capabilities, "_registered_module_available", lambda _module: True)
    report = capabilities.build_capability_report(NOW)
    simulator = next(event for event in report["capabilities"]
                     if event["payload"]["declared_maturity"] == "SIMULATED")
    assert simulator["classification"] == "SIMULATED"
    assert simulator["payload"]["reason"] == "simulator_classification_preserved"


def test_event_envelopes_match_shared_contract(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    records = [evidence_record(entry["capability_id"]) for entry in capabilities.REGISTRY]
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", write_evidence(tmp_path, records))
    monkeypatch.setattr(capabilities, "_registered_module_available", lambda _module: True)
    report = capabilities.build_capability_report(NOW)
    schema_path = REPO_ROOT / "schemas" / "sovereign-event-v1.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    required = set(schema["required"])
    allowed_sources = set(schema["properties"]["source"]["enum"])
    allowed_types = set(schema["properties"]["type"]["enum"])
    allowed_classes = set(schema["properties"]["classification"]["enum"])
    validator = Draft202012Validator(schema, format_checker=Draft202012Validator.FORMAT_CHECKER)
    for event in report["capabilities"]:
        assert required.issubset(event)
        assert set(event).issubset(required | {"correlation_id", "provenance"})
        assert event["schema_version"] == "1.0"
        assert event["source"] in allowed_sources
        assert event["type"] in allowed_types
        assert event["classification"] in allowed_classes
        assert event["timestamp"].endswith("Z")
        assert event["provenance"]["repository"] == "onegayunicorn/unicorn-sovereign-platform"
        assert len(event["provenance"]["revision"]) == 40
        assert list(validator.iter_errors(event)) == []

    # The actual shared schema must reject a non-canonical evidence label.
    invalid_event = dict(report["capabilities"][0])
    invalid_event["classification"] = "PROTOTYPE"
    assert list(validator.iter_errors(invalid_event))


def test_duplicate_evidence_records_fail_closed(tmp_path, monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    item = evidence_record(capabilities.REGISTRY[0]["capability_id"])
    monkeypatch.setenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE",
                       write_evidence(tmp_path, [item, item]))
    report = capabilities.build_capability_report(NOW)
    assert report["status"] == "UNKNOWN"


def test_only_registered_capabilities_are_emitted(monkeypatch):
    monkeypatch.setenv("SOVEREIGN_SOURCE_REVISION", REVISION)
    report = capabilities.build_capability_report(NOW)
    assert {event["payload"]["capability_id"] for event in report["capabilities"]} == {
        entry["capability_id"] for entry in capabilities.REGISTRY
    }
