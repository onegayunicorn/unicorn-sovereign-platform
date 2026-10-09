# Cross-Node API Contracts

All three bridges (Shield Hub, Cognitive Hive, Emu-Verse) share:
- Unified event envelope (see schemas/events.schema.json)
- Signed payloads (Ed25519)
- Idempotency keys on all mutating endpoints
- Env-gated mock/real switch (UNICORN_USE_REAL=true for real endpoints)
