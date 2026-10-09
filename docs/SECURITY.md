# Security posture

- External writes and hardware activation are off by default.
- Tool permissions are declared and checked at runtime; agents cannot grant themselves permissions.
- Destructive, financial, hardware, publication, and external-write actions require a human gate.
- No arbitrary shell execution is exposed to NPC or agent tools.
- Secrets belong in environment variables or a secret manager, never source, logs, or URLs.
- Simulation results must be labelled `Simulated`; never describe them as physical measurements.
- Review dependency, firmware, optical/electrical safety, privacy, and incident response before pilots.
