"""Engine-neutral adapter interface."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

class GameEngineAdapter(ABC):
    @abstractmethod
    def send_dialogue(self, character_id: str, text: str) -> None: ...
    @abstractmethod
    def get_player_input(self, character_id: str) -> str: ...
    @abstractmethod
    def set_behavior_state(self, character_id: str, state: str) -> None: ...
    @abstractmethod
    def emit_event(self, event_type: str, payload: dict) -> None: ...
