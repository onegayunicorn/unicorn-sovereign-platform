"""Idempotency key deduplication — same key → one provider job only."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class IdempotencyStore:
    _keys: Dict[str, str] = field(default_factory=dict)  # key -> job_id

    def check(self, key: str) -> Optional[str]:
        """Return existing job_id if key seen before, else None."""
        return self._keys.get(key)

    def register(self, key: str, job_id: str) -> bool:
        """Register key. Returns False if key already exists (duplicate)."""
        if key in self._keys:
            return False
        self._keys[key] = job_id
        return True
