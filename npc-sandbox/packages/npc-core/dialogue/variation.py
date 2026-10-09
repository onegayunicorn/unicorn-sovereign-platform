"""Response variation layer — prevents repetitive identical responses."""
from __future__ import annotations
import hashlib, time
from typing import List

class VariationLayer:
    def __init__(self):
        self._recent_hashes: list[str] = []

    def vary(self, candidates: List[str]) -> str:
        # Pick a candidate not recently used
        for c in candidates:
            h = hashlib.sha256(c.encode()).hexdigest()[:16]
            if h not in self._recent_hashes:
                self._recent_hashes.append(h)
                if len(self._recent_hashes) > 10:
                    self._recent_hashes.pop(0)
                return c
        return candidates[0] if candidates else ""
