# Tranche #2 — Read-only Capability Reporting

**Maturity: PROTOTYPE.** This endpoint is implemented as a fail-closed API surface. It is not a live integration certification and does not independently authenticate the evidence file.

## Route

- GET /api/v1/capabilities/
- Registered in the existing FastAPI app at unicorn-quantum/apps/api/main.py.
- POST, PUT, and DELETE are not registered for this route.
- No shell, deployment, Git-write, hardware-control, or remote-mutation code is called.

## Evidence inputs

The endpoint has two optional environment inputs:

- SOVEREIGN_SOURCE_REVISION: immutable Git commit SHA (7–64 hexadecimal characters). If absent or invalid, the endpoint returns aggregate UNKNOWN and omits individual capability event claims rather than inventing provenance.
- SOVEREIGN_CAPABILITY_EVIDENCE_FILE: path to a local JSON array of evidence records. File is capped at 256 KB and 100 records. Each record identifies capability_id, status, classification, observed_at, source_revision, evidence_uri, and optional freshness_seconds (1–86400; default 300).

An evidence record is accepted only when its source revision exactly matches the configured revision, its UTC timestamp is fresh, the status/classification are allow-listed, and an evidence URI is present. Missing, malformed, stale, duplicate, or revision-mismatched evidence fails closed to UNKNOWN. A module importability check is also required before a record may report HEALTHY.

**Trust boundary:** the local evidence file is an input record, not a signed attestation. Do not use it as proof of physical hardware operation. Protect its writer and filesystem permissions outside this endpoint; signature verification is a future separately reviewed gate.

## Contract and labels

Each emitted item is a capability.report sovereign-event-v1 envelope with stable source identity, UUID event ID, UTC timestamp, repository/revision provenance, evidence URI, and a bounded JSON payload. Only allow-listed registry entries are emitted. Simulator maturity is preserved as SIMULATED; a generic evidence record cannot promote that component to MEASURED or DEMONSTRATED. PROTOTYPE is retained as declared_maturity metadata and is not falsely inserted into the v1 classification enum.

## Local verification

From the repository root, in an environment with project test dependencies installed:

```bash
python -m pytest quantum/tests/test_capability_endpoint.py -v
python -m pytest quantum/tests/ -v
```

The tests cover default UNKNOWN, valid current evidence, missing revision, stale evidence, revision mismatch, malformed/duplicate input, unavailable modules, label preservation, event-envelope contract fields, and HTTP method restrictions.

## Deployment notes

Set SOVEREIGN_SOURCE_REVISION from the exact deployed Git commit. Configure the evidence file only when a reviewed producer exists. Until then, the expected endpoint result is UNKNOWN with no per-capability claims. Do not configure fabricated fixture evidence in production.

## Rollback

Revert the tranche commit on the development branch. Do not force-push or modify main. If the endpoint is not wanted while review is underway, remove its router inclusion from unicorn-quantum/apps/api/main.py and revert the new module and tests in a visible revert commit.
