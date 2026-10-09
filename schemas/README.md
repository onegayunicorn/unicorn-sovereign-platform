# Shared Contracts — v1.0.0

Single source of truth for the data exchanged between **Unicorndrop Cloud** and the
**Quantum Platform Suite (QPS)**. Four canonical contracts, generated language models,
living fixtures, and CI that validates everything on every PR.

## Contracts

| Schema | Purpose |
| --- | --- |
| `job.schema.json` | Quantum execution job (status, backend, policy, execution options) |
| `circuit.schema.json` | Quantum circuit definition (OpenQASM / QIR / Quil / cirq-json) |
| `artifact.schema.json` | Job-produced artifact (result, compiled circuit, attestation, evidence package, …) |
| `audit-event.schema.json` | Immutable audit event; events sharing a `correlationId` form one lifecycle chain |

## Layout

```
schemas/
├── job.schema.json
├── circuit.schema.json
├── artifact.schema.json
├── audit-event.schema.json
├── fixtures/                # living integration fixtures (Bell-state lifecycle)
├── models/
│   ├── typescript/          # TS interfaces consumed by Unicorndrop / gateway
│   └── python/              # Pydantic models + jsonschema validators consumed by QPS
├── tests/                   # vitest (TS) + pytest (Python)
├── .github/workflows/       # CI: validate TS + Python + correlation chain
├── package.json
├── pyproject.toml
└── README.md
```

## Usage

### TypeScript (Unicorndrop / gateway)

```ts
import type { QuantumJob, AuditEvent } from '@unicorn-schemas/contracts';
```

### Python (QPS)

```python
from schemas.models.python import QuantumJob, validate_against_schema

job = QuantumJob.model_validate(payload)
ok, msg = validate_against_schema(payload, "job")
```

## Local validation

```bash
# TypeScript / JSON Schema
cd schemas && pnpm install && pnpm test

# Python / Pydantic
cd schemas && python -m pip install -e ".[dev]" && pytest tests/validate-python.py -v
```

## Guarantees

- Every PR runs both TypeScript + Python validation automatically.
- No mismatched Job / Circuit / Artifact / Audit definitions between Unicorndrop and QPS.
- `correlationId` is enforced end-to-end — the 7-event Bell-state chain is a living integration test.
