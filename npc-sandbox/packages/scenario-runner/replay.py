"""Deterministic replay of scenario runs."""
from __future__ import annotations
import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class ReplayRecord:
    step_index: int
    player_input: str
    npc_response: str
    safety_passed: bool
    behavior_state: str

class DeterministicReplay:
    def __init__(self):
        self._records: List[ReplayRecord] = []

    def record(self, rec: ReplayRecord) -> None:
        self._records.append(rec)

    def export(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump([asdict(r) for r in self._records], f, indent=2)

    def verify_deterministic(self, other: "DeterministicReplay") -> bool:
        return [asdict(r) for r in self._records] == [asdict(r) for r in other._records]
