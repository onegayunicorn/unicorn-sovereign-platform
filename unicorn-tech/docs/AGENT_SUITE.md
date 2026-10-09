# 6-Agent Governance Model

| Agent | Produces | Forbidden |
|-------|----------|-----------|
| Architect | System designs, interface maps, decision records, risk registers, deployment gates | Authorize global deployment |
| Integrator | Node APIs, event schemas, telemetry adapters, retry handling, orchestration workflows | Rotate production keys |
| Security | Threat models, key lifecycle plans, config reviews, supply-chain findings, approval checklists | Operate high-voltage equipment |
| Quantum-HPC | Benchmark plans, reproducibility reports, simulation comparisons, statistical review, evidence classifications | Claim experimental proof |
| Photonics | Optical experiment plans, calibration procedures, detector characterization, link budgets, measurement reports | Authorize global deployment |
| Repository | Source files, schemas, CI workflows, documentation, test fixtures, PR drafts | Merge without review |

No agent may independently authorize global deployment, claim experimental proof,
rotate production keys, or operate high-voltage equipment.
