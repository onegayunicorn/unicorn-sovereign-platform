"""Prompt version registry."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class PromptVersion:
    prompt_id: str
    version: int
    text: str
    variables: List[str] = field(default_factory=list)
    checksum: str = ""

class PromptRegistry:
    def __init__(self):
        self._prompts: Dict[str, List[PromptVersion]] = {}

    def add(self, pv: PromptVersion) -> None:
        self._prompts.setdefault(pv.prompt_id, []).append(pv)

    def latest(self, prompt_id: str) -> PromptVersion | None:
        versions = self._prompts.get(prompt_id, [])
        return max(versions, key=lambda v: v.version) if versions else None
