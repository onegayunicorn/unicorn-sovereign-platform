"""Intent detection + context window management."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class DialogueTurn:
    speaker: str  # player / npc
    text: str
    intent: str = "unknown"
    timestamp: float = 0.0

class DialogueManager:
    MAX_CONTEXT_TURNS = 20

    def __init__(self, character_id: str):
        self.character_id = character_id
        self._history: List[DialogueTurn] = []

    def add_player_turn(self, text: str, intent: str = "unknown") -> None:
        self._history.append(DialogueTurn("player", text, intent))
        self._trim()

    def add_npc_turn(self, text: str) -> None:
        self._history.append(DialogueTurn("npc", text))
        self._trim()

    def _trim(self) -> None:
        if len(self._history) > self.MAX_CONTEXT_TURNS:
            self._history = self._history[-self.MAX_CONTEXT_TURNS:]

    def context_window(self) -> List[DialogueTurn]:
        return list(self._history)

    def detect_intent(self, text: str) -> str:
        t = text.lower()
        if any(w in t for w in ["quest", "mission", "task", "help"]):
            return "quest"
        if any(w in t for w in ["bye", "goodbye", "leave", "exit"]):
            return "farewell"
        if any(w in t for w in ["who", "what", "where", "how", "why"]):
            return "question"
        if any(w in t for w in ["trade", "buy", "sell", "item"]):
            return "trade"
        return "smalltalk"
