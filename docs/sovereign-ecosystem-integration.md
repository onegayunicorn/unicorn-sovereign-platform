# Sovereign Ecosystem Integration

This document describes the proposed read-only integration boundary between Unicorn Sovereign Platform, Photonic Codex, and Quantum Multiversal Nexus.

## Authority and responsibilities

- **Platform** is authoritative for its own runtime module status and test/simulation results.
- **Photonic Codex** is authoritative for local operational events and its provenance records.
- **Nexus** is a manifest and display layer; it cannot upgrade evidence labels or infer a healthy status from missing data.

Each system retains its own repository history, release process, and tests.

## Shared event contract

The shared contract is documented in [sovereign-event-contract-v1.md](sovereign-event-contract-v1.md). Use the same envelope, UTC timestamps, event identifiers, evidence labels, and provenance fields. The contract is proposed until consumer/producer contract tests pass.

Canonical evidence labels are `PROPOSED`, `SIMULATED`, `DEMONSTRATED`, `MEASURED`, `UNVERIFIED`, and `VALIDATED`. Do not silently map labels. Preserve an unknown source label verbatim and flag it as unmapped.

## Initial API shape

A future adapter may expose a read-only capability report:

```json
{
  "schema_version": "1.0",
  "source": "unicorn-sovereign-platform",
  "observed_at": "2026-10-11T00:00:00Z",
  "source_revision": "git-commit-sha",
  "status": "UNKNOWN",
  "capabilities": []
}
```

This is a contract example, not a claim that the endpoint currently exists. The adapter must only report verified local information and must not return a healthy status when checks fail or evidence is stale.

## Safety requirements

1. Read-only access is the initial integration mode.
2. External endpoints must be explicitly configured and authenticated; never embed credentials in source.
3. Validate schema, payload size, timestamp, source identity, and supported schema version.
4. Network errors, stale results, and invalid payloads become UNKNOWN/UNAVAILABLE, never healthy.
5. No remote command execution, deployment, rollback, Git push, or hardware-control messages in v1.
6. Simulation remains `SIMULATED`; source labels and provenance are preserved end-to-end.
7. Contract tests and negative-path tests are required before enabling live polling.

## Cross-repository links

- [Photonic Codex](https://github.com/onegayunicorn/photonic-codex)
- [Quantum Multiversal Nexus](https://github.com/onegayunicorn/quantum-multiversal-nexus)
