# Unicorn Quantum Platform

Capability: IMPLEMENTED. Python (API/workers) + TypeScript (web).

## Job State Machine
DRAFT → VALIDATING → VALIDATED → COMPILING → COMPILED → QUEUED → SUBMITTED → RUNNING → COMPLETED
Terminal: FAILED | CANCELLED | EXPIRED | RETRYING

## Acceptance Tests (must all pass)
- Bell state: ~50% |00⟩ / ~50% |11⟩ with 1024 shots
- OpenQASM 2 round-trip: import → IR → export → re-parse → semantic equivalence
- Idempotency: same key → one provider job only
- Recovery: kill worker → restart → result persisted exactly once
