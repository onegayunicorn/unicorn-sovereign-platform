# Unicorn Sovereign Platform

**A modular sovereign runtime for AI orchestration, NPC sandboxing, edge/cloud services, and quantum/photonic simulation.**

> **Evidence note:** This README is an architecture overview, not an independent release certification. Each module's maturity must be supported by current tests and evidence. Quantum/photonic Stage 0 is simulation; prototype or hardware claims require separate validation.

## Core principle

Components should be independently buildable, locally runnable where supported, and deployable without mandatory cloud lock-in. Report actual build/test status and known limitations for each release.

## Modules

| Module | Path | Language | Declared scope |
|---|---|---|---|
| Quantum Photonic | `quantum/` | Python 3.12+ | Stage 0 simulation; higher stages require evidence |
| AI Orchestration | `ai-orchestration/` | Python 3.12+ | Orchestration runtime |
| NPC Sandbox | `npc-sandbox/` | TypeScript | NPC simulation and interaction |
| Unicorn Quantum Platform | `unicorn-quantum/` | Python + TypeScript | Quantum-related simulation/platform code |
| Cerebral Matrix OS | `cerebral-matrix/` | TypeScript + Python | Cognitive/matrix services |
| Unicorndrop Cloud | `unicorndrop/` | TypeScript + Go | Cloud file/service components |
| UnicornCloud Edge | `unicorn-cloud/` | TypeScript (Cloudflare Workers) | Edge service components |
| Unicorn Tech / Φ⁵ Console | `unicorn-tech/` | TypeScript | Console and operator interface |
| Automation Monitor Suite | `automation-monitor/` | Python 3.12+ | Monitoring and automation |
| Shared Infrastructure | `infra/` | Docker / Kubernetes / Terraform | Deployment definitions |

Directory presence and a successful process start do not establish production readiness. Consult each module's tests, CI evidence, and release notes before relying on it.

## Quick start

Review `.env.example` and the Compose configuration before running:

```bash
cp .env.example .env
docker compose up --build
```

Do not commit `.env` or production secrets.

## Shared evidence classification

The cross-repository contract is [docs/sovereign-event-contract-v1.md](docs/sovereign-event-contract-v1.md). The integration boundary and proposed read-only API shape are described in [docs/sovereign-ecosystem-integration.md](docs/sovereign-ecosystem-integration.md).

Canonical labels: **PROPOSED / SIMULATED / DEMONSTRATED / MEASURED / UNVERIFIED / VALIDATED**. Preserve source labels and provenance. Never promote a simulated result to measured hardware evidence.

## Related repositories

- [Photonic Codex](https://github.com/onegayunicorn/photonic-codex) — local operations, dashboard, events, and provenance.
- [Quantum Multiversal Nexus](https://github.com/onegayunicorn/quantum-multiversal-nexus) — ecosystem manifest and read-only status presentation.

The FastAPI prototype exposes GET /api/v1/capabilities/ from unicorn-quantum/apps/api/main.py. It defaults to UNKNOWN and omits per-capability event claims until an immutable source revision is configured. Current evidence-file handling is a local prototype, not a signed attestation. Cross-repository live integration is not established merely by adding links or contract documents.
