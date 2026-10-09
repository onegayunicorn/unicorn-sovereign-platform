# UnicornCloud Edge

Capability: IMPLEMENTED. TypeScript on Cloudflare Workers.

## State Primitive Rules
- D1 SQL = transactional source of truth (never KV)
- Durable Objects = per-tenant coordination + locks
- KV = eventual-consistency cache/config only — never sole source of truth for money/permissions
- R2 = artifacts + uploads (immutable by content hash); SQL tracks ownership
