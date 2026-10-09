"""Content policy rules."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class ContentPolicy:
    forbidden_patterns: List[str]
    max_response_length: int = 2000

    def check(self, text: str) -> tuple[bool, str]:
        lower = text.lower()
        for p in self.forbidden_patterns:
            if p.lower() in lower:
                return False, f"violates policy: {p}"
        if len(text) > self.max_response_length:
            return False, "response too long"
        return True, "ok"
