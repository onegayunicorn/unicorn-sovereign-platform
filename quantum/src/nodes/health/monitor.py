"""Telemetry + alarms — temperature, pump power, detector health, dark counts, coincidence rates, timing drift, packet loss, optical power, CPU/memory, firmware state, security alerts."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List
import time

@dataclass
class TelemetrySample:
    node_id: str
    timestamp: float
    temperature_c: float = 0.0
    pump_power_mw: float = 0.0
    dark_count_hz: float = 0.0
    coincidence_rate_hz: float = 0.0
    timing_drift_ppb: float = 0.0
    packet_loss_pct: float = 0.0
    optical_power_dbm: float = 0.0
    cpu_pct: float = 0.0
    memory_pct: float = 0.0
    firmware_ok: bool = True
    security_alert: bool = False

@dataclass
class Alarm:
    node_id: str
    metric: str
    value: float
    threshold: float
    severity: str  # info / warning / critical
    timestamp: float

class HealthMonitor:
    def __init__(self):
        self._alarms: List[Alarm] = []

    def check(self, sample: TelemetrySample, thresholds: Dict[str, float]) -> List[Alarm]:
        now = time.time()
        new_alarms = []
        for metric, threshold in thresholds.items():
            value = getattr(sample, metric, None)
            if isinstance(value, (int, float)) and value > threshold:
                alarm = Alarm(sample.node_id, metric, value, threshold, "warning", now)
                new_alarms.append(alarm)
                self._alarms.append(alarm)
        if sample.security_alert:
            alarm = Alarm(sample.node_id, "security", 1.0, 0.5, "critical", now)
            new_alarms.append(alarm)
            self._alarms.append(alarm)
        return new_alarms

    @property
    def alarms(self) -> List[Alarm]:
        return list(self._alarms)
