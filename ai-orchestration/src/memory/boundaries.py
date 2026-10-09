"""Memory scope limits + expiration."""
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class MemoryEntry:
    key: str
    value: str
    scope: str  # session / tenant / agent / global
    created_at: float
    expires_at: Optional[float] = None
    tenant_id: Optional[str] = None
    agent_id: Optional[str] = None

class MemoryStore:
    MAX_SESSION_ENTRIES = 1000
    MAX_TENANT_ENTRIES = 10000

    def __init__(self):
        self._store: Dict[str, MemoryEntry] = {}

    def _scope_key(self, entry: MemoryEntry) -> str:
        return f"{entry.scope}:{entry.tenant_id or ''}:{entry.agent_id or ''}:{entry.key}"

    def put(self, entry: MemoryEntry) -> bool:
        # Enforce scope limits
        scope_count = sum(1 for e in self._store.values()
                          if e.scope == entry.scope and e.tenant_id == entry.tenant_id)
        limit = self.MAX_SESSION_ENTRIES if entry.scope == "session" else self.MAX_TENANT_ENTRIES
        if scope_count >= limit:
            return False
        self._store[self._scope_key(entry)] = entry
        return True

    def get(self, scope: str, key: str, tenant_id: str | None = None,
            agent_id: str | None = None) -> MemoryEntry | None:
        sk = f"{scope}:{tenant_id or ''}:{agent_id or ''}:{key}"
        entry = self._store.get(sk)
        if entry and entry.expires_at and entry.expires_at < time.time():
            del self._store[sk]
            return None
        return entry
