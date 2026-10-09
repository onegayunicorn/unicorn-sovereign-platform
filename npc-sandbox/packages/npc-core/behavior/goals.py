"""Goal system with priority + cooldowns."""
from __future__ import annotations
from dataclasses import dataclass, field
import time
from typing import List

@dataclass
class Goal:
    goal_id: str
    description: str
    priority: int = 5  # 1-10, higher = more important
    cooldown_seconds: float = 60.0
    last_activated: float = 0.0

    def can_activate(self) -> bool:
        return time.time() - self.last_activated >= self.cooldown_seconds

    def activate(self) -> None:
        self.last_activated = time.time()

class GoalSystem:
    def __init__(self):
        self._goals: List[Goal] = []

    def add(self, goal: Goal) -> None:
        self._goals.append(goal)

    def select_next(self) -> Goal | None:
        available = [g for g in self._goals if g.can_activate()]
        if not available:
            return None
        return max(available, key=lambda g: g.priority)
