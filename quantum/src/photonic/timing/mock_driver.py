"""Mock timing driver."""
from __future__ import annotations
import time
from .interface import TimingHardware

class MockTimingHardware(TimingHardware):
    def __init__(self):
        self._offset = 0
        self._drift_ppb = 1.0

    def sync(self) -> bool:
        self._offset = 0
        return True

    def now_ns(self) -> int:
        return time.time_ns() + self._offset

    def clock_drift_ppb(self) -> float:
        return self._drift_ppb

    def holdover_seconds(self) -> float:
        return 3600.0

    def trigger_out(self, channel: int) -> None:
        pass
