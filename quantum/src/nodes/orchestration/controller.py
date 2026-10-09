"""Experiment controller — runs the full experiment lifecycle."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List
from enum import Enum

class ExperimentState(str, Enum):
    PENDING = "pending"
    CONFIGURING = "configuring"
    CALIBRATING = "calibrating"
    RUNNING = "running"
    COLLECTING = "collecting"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"

@dataclass
class ExperimentControl:
    experiment_id: str
    node_ids: List[str]
    state: ExperimentState = ExperimentState.PENDING

    def transition(self, new_state: ExperimentState) -> None:
        self.state = new_state

    def abort(self) -> None:
        self.state = ExperimentState.ABORTED
