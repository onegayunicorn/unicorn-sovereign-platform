"""Deterministic test driver."""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import yaml

@dataclass
class ScenarioStep:
    player_input: str
    expected_npc_intent: str = ""
    expected_behavior_state: str = ""

@dataclass
class Scenario:
    scenario_id: str
    character_id: str
    steps: List[ScenarioStep]

class ScenarioHarness:
    def __init__(self, engine):
        self.engine = engine

    def load(self, path: str) -> Scenario:
        with open(path) as f:
            data = yaml.safe_load(f)
        steps = [ScenarioStep(**s) for s in data.get("steps", [])]
        return Scenario(scenario_id=data["scenario_id"], character_id=data["character_id"], steps=steps)
