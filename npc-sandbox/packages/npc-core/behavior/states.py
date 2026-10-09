"""FSM states: Idle/Patrol/Converse/Quest/Combat/Flee."""
from __future__ import annotations
from enum import Enum

class BehaviorState(str, Enum):
    IDLE = "idle"
    PATROL = "patrol"
    CONVERSE = "converse"
    QUEST = "quest"
    COMBAT = "combat"
    FLEE = "flee"
    SLEEP = "sleep"
