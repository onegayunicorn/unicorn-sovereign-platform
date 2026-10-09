"""Dialogue state tracking."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class DialoguePhase(str, Enum):
    GREETING = "greeting"
    CONVERSING = "conversing"
    QUEST_OFFER = "quest_offer"
    QUEST_ACTIVE = "quest_active"
    FAREWELL = "farewell"

@dataclass
class DialogueState:
    phase: DialoguePhase = DialoguePhase.GREETING
    turn_count: int = 0
    last_intent: str = "none"
    flags: dict = field(default_factory=dict)

    def transition(self, new_phase: DialoguePhase) -> None:
        self.phase = new_phase
