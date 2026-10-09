# Cerebral Matrix OS

Capability: IMPLEMENTED. PWA — runs fully offline after first install.

## PQC Algorithms (NIST standard — never invent crypto)
- ML-KEM-768 (key encapsulation)
- ML-DSA-65 (digital signatures)
- SLH-DSA-SHA2-128s (hash-based signatures)
- Hybrid: ML-KEM-768 + ECDSA-P256 for browser interoperability

## PWA Requirements (all mandatory)
- Runs fully offline after first install
- No telemetry by default — every outbound request is opt-in
- Export + delete controls for all locally stored data
- No secrets in source, artifacts, logs, or URLs
