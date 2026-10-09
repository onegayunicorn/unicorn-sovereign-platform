"""State transition rules."""
from __future__ import annotations
from .states import BehaviorState

# Allowed transitions (from -> set of valid next states)
TRANSITIONS: dict[BehaviorState, set[BehaviorState]] = {
    BehaviorState.IDLE: {BehaviorState.PATROL, BehaviorState.CONVERSE, BehaviorState.SLEEP, BehaviorState.FLEE},
    BehaviorState.PATROL: {BehaviorState.IDLE, BehaviorState.CONVERSE, BehaviorState.COMBAT, BehaviorState.FLEE},
    BehaviorState.CONVERSE: {BehaviorState.IDLE, BehaviorState.QUEST, BehaviorState.PATROL},
    BehaviorState.QUEST: {BehaviorState.IDLE, BehaviorState.CONVERSE, BehaviorState.COMBAT},
    BehaviorState.COMBAT: {BehaviorState.FLEE, BehaviorState.IDLE, BehaviorState.QUEST},
    BehaviorState.FLEE: {BehaviorState.IDLE, BehaviorState.SLEEP},
    BehaviorState.SLEEP: {BehaviorState.IDLE, BehaviorState.PATROL},
}

def can_transition(current: BehaviorState, next_state: BehaviorState) -> bool:
    return next_state in TRANSITIONS.get(current, set())
