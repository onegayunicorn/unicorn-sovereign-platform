"""Graceful disabled state — when safety triggers, NPC enters safe mode."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class DisabledState:
    active: bool = False
    reason: str = ""
    graceful_response: str = "I'm unable to continue this conversation right now. Please try a different topic."

    def trigger(self, reason: str) -> None:
        self.active = True
        self.reason = reason

    def reset(self) -> None:
        self.active = False
        self.reason = ""

    def respond(self) -> str:
        return self.graceful_response
