# CODE_NOTES — Tranche #2 Capability Reporting

## Changed surface

- unicorn-quantum/apps/api/api/v1/capabilities.py — read-only report builder and GET router.
- unicorn-quantum/apps/api/main.py — mounts the route.
- unicorn-quantum/apps/api/api/v1/circuits.py and jobs.py — correct package imports so the existing API can be imported and tested from the repository root.
- ai-orchestration/src/tools/permissions.py — corrects a pre-existing import that broke its existing security test collection.
- quantum/tests/test_capability_endpoint.py — endpoint and failure-path tests.
- pyproject.toml — adds PEP 621 metadata, explicit setuptools package discovery, and installable dev dependencies so the existing CI install command can work.
- docs/tranche-2-capability-endpoint.md — configuration, evidence rules, trust boundary, tests, and rollback.

## Safety boundaries

- The only new HTTP route is GET /api/v1/capabilities/.
- No shell execution, remote polling, deployment, Git write, or hardware activation.
- No source revision means no per-capability event claims are emitted.
- Evidence must be fresh and revision-matched; stale, malformed, duplicate, unavailable, or mismatched data fails closed.
- Local JSON evidence is not cryptographically authenticated and must not be treated as a signed attestation.
- SIMULATED components cannot be relabelled MEASURED or DEMONSTRATED by generic evidence input.
- Existing broken imports were corrected only to make existing modules importable and their tests collect.

## Maturity

PROTOTYPE. The endpoint has been committed to the development branch. CI must complete green and evidence-file trust must be reviewed before the PR is marked ready. No merge to main has been performed.
