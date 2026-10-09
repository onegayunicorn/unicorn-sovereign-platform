# Unicorn Tech Integration — Φ⁵ Console

Capability: IMPLEMENTED. Bridges to N01 Shield Hub, N02 Cognitive Hive, N03 Emu-Verse.
Env-gated mock/real switch — all real endpoints require explicit opt-in.

## Telemetry Refresh Intervals
| Panel | Source | Interval | Endpoint |
|-------|--------|----------|----------|
| Topology / Uptime | Shield Hub | 4s | /telemetry |
| Agent Status | Cognitive Hive | 8s | /twins/status |
| Runtime Metrics | Emu-Verse | 1.5s | /runtime/status |
| Safety Log | Shield Hub | 15s poll | /safety/gate/log |
