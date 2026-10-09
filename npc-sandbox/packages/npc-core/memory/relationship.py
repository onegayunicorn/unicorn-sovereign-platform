"""Player relationship state."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class RelationshipState:
    player_id: str
    trust: float = 0.0       # -1.0 to 1.0
    familiarity: int = 0     # number of interactions
    reputation: float = 0.0

    def update_trust(self, delta: float) -> None:
        self.trust = max(-1.0, min(1.0, self.trust + delta))

    def increment_interaction(self) -> None:
        self.familiarity += 1
