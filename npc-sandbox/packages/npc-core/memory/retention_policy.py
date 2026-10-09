"""Auto-expiration policies for memory."""
from __future__ import annotations
import time
from dataclasses import dataclass

@dataclass
class RetentionPolicy:
    session_ttl_seconds: float = 3600.0
    long_term_max_entries: int = 100
    quest_ttl_seconds: float = 86400.0 * 30  # 30 days

    def is_expired(self, created_at: float, ttl: float) -> bool:
        return time.time() - created_at > ttl
