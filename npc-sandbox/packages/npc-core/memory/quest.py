"""Quest memory."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum

class QuestStatus(str, Enum):
    UNOFFERED = "unoffered"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class QuestMemory:
    quests: Dict[str, QuestStatus] = field(default_factory=dict)

    def set_status(self, quest_id: str, status: QuestStatus) -> None:
        self.quests[quest_id] = status

    def active_quests(self) -> List[str]:
        return [q for q, s in self.quests.items() if s == QuestStatus.IN_PROGRESS]
