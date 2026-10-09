"""Headless test harness — mock game engine."""
from __future__ import annotations
from .interface import GameEngineAdapter
from typing import List, Dict

class MockGameEngine(GameEngineAdapter):
    def __init__(self):
        self.dialogue_log: List[Dict] = []
        self.events: List[Dict] = []
        self.behavior_states: Dict[str, str] = {}
        self._player_input_queue: List[str] = []

    def queue_player_input(self, text: str) -> None:
        self._player_input_queue.append(text)

    def send_dialogue(self, character_id: str, text: str) -> None:
        self.dialogue_log.append({"character": character_id, "text": text})

    def get_player_input(self, character_id: str) -> str:
        return self._player_input_queue.pop(0) if self._player_input_queue else ""

    def set_behavior_state(self, character_id: str, state: str) -> None:
        self.behavior_states[character_id] = state

    def emit_event(self, event_type: str, payload: dict) -> None:
        self.events.append({"type": event_type, "payload": payload})
