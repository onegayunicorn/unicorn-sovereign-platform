"""Job state machine + transitions."""
from __future__ import annotations
from ..domain.job import JobStatus
from typing import Set

# Allowed transitions
TRANSITIONS: dict[JobStatus, Set[JobStatus]] = {
    JobStatus.DRAFT: {JobStatus.VALIDATING, JobStatus.CANCELLED},
    JobStatus.VALIDATING: {JobStatus.VALIDATED, JobStatus.FAILED, JobStatus.CANCELLED},
    JobStatus.VALIDATED: {JobStatus.COMPILING, JobStatus.CANCELLED, JobStatus.EXPIRED},
    JobStatus.COMPILING: {JobStatus.COMPILED, JobStatus.FAILED, JobStatus.CANCELLED},
    JobStatus.COMPILED: {JobStatus.QUEUED, JobStatus.CANCELLED, JobStatus.EXPIRED},
    JobStatus.QUEUED: {JobStatus.SUBMITTED, JobStatus.CANCELLED, JobStatus.EXPIRED, JobStatus.RETRYING},
    JobStatus.SUBMITTED: {JobStatus.RUNNING, JobStatus.FAILED, JobStatus.CANCELLED, JobStatus.RETRYING},
    JobStatus.RUNNING: {JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED, JobStatus.RETRYING},
    JobStatus.RETRYING: {JobStatus.QUEUED, JobStatus.FAILED},
    JobStatus.COMPLETED: set(), JobStatus.FAILED: set(),
    JobStatus.CANCELLED: set(), JobStatus.EXPIRED: set(),
}

TERMINAL_STATES = {JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED, JobStatus.EXPIRED}

class InvalidTransition(Exception):
    pass

def can_transition(current: JobStatus, next_state: JobStatus) -> bool:
    return next_state in TRANSITIONS.get(current, set())

def transition(current: JobStatus, next_state: JobStatus) -> JobStatus:
    if not can_transition(current, next_state):
        raise InvalidTransition(f"{current} -> {next_state} not allowed")
    return next_state
