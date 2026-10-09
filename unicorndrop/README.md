# Unicorndrop Cloud

Capability: IMPLEMENTED. Sovereign file transfer — TypeScript services + Go gateways.

## Transfer State Machine
CREATED -> ACCEPTING -> RECEIVED -> SCANNING -> APPROVED -> DELIVERING -> DELIVERED
Terminal: REJECTED | QUARANTINED | DEAD_LETTERED

## Every transfer must have
- idempotency key
- SHA-256 content hash
- immutable audit trail
- retry classification (transient / auth / policy / permanent)
