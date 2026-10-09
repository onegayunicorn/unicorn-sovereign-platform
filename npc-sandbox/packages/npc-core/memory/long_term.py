"""Long-term memory summaries."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

@dataclass
class LongTermMemory:
    character_id: str
    summaries: List[str] = field(default_factory=list)

    def add_summary(self, summary: str) -> None:
        self.summaries.append(summary)
        if len(self.summaries) > 100:
            # Compress: merge oldest
            self.summaries = [" | ".join(self.summaries[:2])] + self.summaries[2:]
