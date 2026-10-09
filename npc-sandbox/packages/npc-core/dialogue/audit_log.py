"""Immutable audit logger for NPC dialogue."""
from __future__ import annotations
import json, hashlib, time
from dataclasses import dataclass

@dataclass
class AuditEntry:
    seq: int
    timestamp: float
    player_input_hash: str
    npc_output_hash: str
    safety_gate_passed: bool
    prev_hash: str | None
    entry_hash: str = ""

class ImmutableAuditLog:
    def __init__(self):
        self._entries: list[AuditEntry] = []
        self._last_hash: str | None = None

    def append(self, player_input: str, npc_output: str, safety_passed: bool) -> AuditEntry:
        seq = len(self._entries)
        entry = AuditEntry(
            seq=seq, timestamp=time.time(),
            player_input_hash=hashlib.sha256(player_input.encode()).hexdigest(),
            npc_output_hash=hashlib.sha256(npc_output.encode()).hexdigest(),
            safety_gate_passed=safety_passed,
            prev_hash=self._last_hash,
        )
        payload = f"{seq}{entry.timestamp}{entry.player_input_hash}{entry.npc_output_hash}{entry.prev_hash}"
        entry.entry_hash = hashlib.sha256(payload.encode()).hexdigest()
        self._last_hash = entry.entry_hash
        self._entries.append(entry)
        return entry

    @property
    def entries(self):
        return list(self._entries)
