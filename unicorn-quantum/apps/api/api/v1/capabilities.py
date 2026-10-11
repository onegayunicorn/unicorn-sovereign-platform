"""Read-only, fail-closed capability reporting for the Platform API.

Evidence is consumed from an explicitly configured local JSON file. No remote
polling, command execution, writes, deployment, or hardware activation occurs.
An evidence file is an input record, not a cryptographic attestation.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter

router = APIRouter()
SOURCE = "unicorn-sovereign-platform"
REPOSITORY = "onegayunicorn/unicorn-sovereign-platform"
HEALTH_VALUES = {"HEALTHY", "DEGRADED", "UNAVAILABLE", "UNKNOWN"}
CLASSIFICATIONS = {
    "PROPOSED", "SIMULATED", "DEMONSTRATED", "MEASURED", "UNVERIFIED", "VALIDATED"
}
REVISION_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")
DEFAULT_FRESHNESS_SECONDS = 300

# This is an allow-list of registered components, not a declaration that they
# are operational. Presence is observed separately; status requires evidence.
REGISTRY = (
    {
        "capability_id": "quantum.state_vector_simulator",
        "module": "packages.provider.simulator.state_vector",
        "declared_maturity": "SIMULATED",
    },
    {
        "capability_id": "quantum.job_state_machine",
        "module": "packages.execution.state_machine",
        "declared_maturity": "PROTOTYPE",
    },
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.endswith("Z"):
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
        return parsed if parsed.tzinfo is not None else None
    except ValueError:
        return None


def _source_revision() -> str | None:
    value = os.getenv("SOVEREIGN_SOURCE_REVISION", "").strip()
    return value if REVISION_RE.fullmatch(value) else None


def _registered_module_available(module_name: str) -> bool:
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError, ValueError, AttributeError):
        return False


def _load_evidence() -> tuple[dict[str, dict[str, Any]], str | None]:
    """Load a bounded local evidence file; malformed/unreadable input fails closed."""
    configured = os.getenv("SOVEREIGN_CAPABILITY_EVIDENCE_FILE", "").strip()
    if not configured:
        return {}, "evidence_source_not_configured"
    try:
        path = Path(configured)
        if not path.is_file() or path.stat().st_size > 256_000:
            return {}, "evidence_source_missing_or_too_large"
        raw = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, list) or len(raw) > 100:
            return {}, "evidence_source_malformed"
        records: dict[str, dict[str, Any]] = {}
        for item in raw:
            if not isinstance(item, dict):
                return {}, "evidence_source_malformed"
            key = item.get("capability_id")
            if not isinstance(key, str) or key in records:
                return {}, "evidence_source_malformed"
            records[key] = item
        return records, None
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}, "evidence_source_unreadable"


def _evaluate(entry: dict[str, str], evidence: dict[str, Any] | None,
              revision: str | None, load_error: str | None,
              now: datetime | None = None) -> dict[str, Any]:
    now = now or _utc_now()
    module_available = _registered_module_available(entry["module"])
    status = "UNKNOWN"
    classification = "UNVERIFIED"
    reason = load_error or "evidence_missing"
    observed_at = _iso_z(now)
    evidence_uri = None

    if evidence is not None and revision is not None:
        source_revision = evidence.get("source_revision")
        evidence_time = _parse_time(evidence.get("observed_at"))
        evidence_status = evidence.get("status")
        evidence_classification = evidence.get("classification")
        uri = evidence.get("evidence_uri")
        freshness = evidence.get("freshness_seconds", DEFAULT_FRESHNESS_SECONDS)
        valid_freshness = isinstance(freshness, int) and not isinstance(freshness, bool) and 1 <= freshness <= 86400
        age = (now - evidence_time).total_seconds() if evidence_time else None

        if (
            source_revision == revision
            and REVISION_RE.fullmatch(str(source_revision or "")) is not None
            and evidence_time is not None
            and age is not None
            and valid_freshness
            and -30 <= age <= freshness
            and isinstance(evidence_status, str)
            and evidence_status in HEALTH_VALUES
            and isinstance(evidence_classification, str)
            and evidence_classification in CLASSIFICATIONS
            and isinstance(uri, str)
            and 1 <= len(uri) <= 2048
        ):
            status = evidence_status
            classification = evidence_classification
            observed_at = _iso_z(evidence_time)
            evidence_uri = uri
            reason = "current_revision_linked_evidence"
            if not module_available and status == "HEALTHY":
                status = "UNKNOWN"
                reason = "registered_module_not_importable"
        else:
            reason = "evidence_invalid_stale_or_revision_mismatch"
    elif revision is None:
        reason = "source_revision_unavailable"

    # Simulation is a property of the component and must not be promoted to
    # physical/measured evidence by a generic health record.
    if entry["declared_maturity"] == "SIMULATED" and classification in {"MEASURED", "DEMONSTRATED"}:
        classification = "SIMULATED"
        reason = "simulator_classification_preserved"

    return {
        "capability_id": entry["capability_id"],
        "module": entry["module"],
        "module_available": module_available,
        "status": status,
        "classification": classification,
        "declared_maturity": entry["declared_maturity"],
        "observed_at": observed_at,
        "evidence_uri": evidence_uri,
        "reason": reason,
    }


def build_capability_report(now: datetime | None = None) -> dict[str, Any]:
    """Return contract envelopes and aggregate health; no state is mutated."""
    now = now or _utc_now()
    revision = _source_revision()
    records, load_error = _load_evidence()
    reports = [
        _evaluate(entry, records.get(entry["capability_id"]), revision, load_error, now)
        for entry in REGISTRY
    ]

    statuses = [item["status"] for item in reports]
    if statuses and all(status == "HEALTHY" for status in statuses):
        aggregate_status = "HEALTHY"
    elif any(status == "UNAVAILABLE" for status in statuses):
        aggregate_status = "UNAVAILABLE"
    elif any(status == "DEGRADED" for status in statuses):
        aggregate_status = "DEGRADED"
    else:
        aggregate_status = "UNKNOWN"

    # The contract requires revision-linked provenance for capability claims.
    # Without an immutable source revision, publish UNKNOWN summary only and
    # omit per-capability event claims rather than inventing provenance.
    if revision is None:
        return {
            "schema_version": "1.0",
            "source": SOURCE,
            "observed_at": _iso_z(now),
            "source_revision": None,
            "status": "UNKNOWN",
            "reason": "source_revision_unavailable",
            "registered_capability_count": len(REGISTRY),
            "capabilities": [],
        }

    events = []
    for item in reports:
        events.append({
            "schema_version": "1.0",
            "event_id": str(uuid.uuid4()),
            "timestamp": _iso_z(now),
            "source": SOURCE,
            "type": "capability.report",
            "classification": item["classification"],
            "correlation_id": None,
            "provenance": {
                "repository": REPOSITORY,
                "revision": revision,
                "evidence_uri": item["evidence_uri"],
            },
            "payload": {
                "capability_id": item["capability_id"],
                "module": item["module"],
                "module_available": item["module_available"],
                "status": item["status"],
                "observed_at": item["observed_at"],
                "source_revision": revision,
                "declared_maturity": item["declared_maturity"],
                "reason": item["reason"],
            },
        })

    return {
        "schema_version": "1.0",
        "source": SOURCE,
        "observed_at": _iso_z(now),
        "source_revision": revision,
        "status": aggregate_status,
        "capabilities": events,
    }


@router.get("/", name="list_capabilities")
def list_capabilities() -> dict[str, Any]:
    """Read-only capability report. Missing/stale evidence is always UNKNOWN."""
    return build_capability_report()
