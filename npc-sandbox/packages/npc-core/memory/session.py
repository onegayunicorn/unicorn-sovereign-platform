"""Session memory (ephemeral)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class SessionMemory:
    session_id: str
    facts: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=__import__("time").time)

    def remember(self, key: str, value: Any) -> None:
        self.facts[key] = value

    def recall(self, key: str) -> Any | None:
        return self.facts.get(key)
