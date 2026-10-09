-- D1 SQL migration — expand/backfill/switch pattern.
-- D1 = transactional source of truth. Never use KV for money/permissions.
CREATE TABLE IF NOT EXISTS tenants (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  plan TEXT NOT NULL DEFAULT 'free',
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
  content_hash TEXT PRIMARY KEY,  -- immutable by content hash
  owner_tenant_id TEXT NOT NULL REFERENCES tenants(id),
  size_bytes INTEGER NOT NULL,
  r2_key TEXT NOT NULL,
  created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_artifacts_owner ON artifacts(owner_tenant_id);
