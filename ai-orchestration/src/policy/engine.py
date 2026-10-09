"""Policy evaluation engine."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, List

@dataclass
class Policy:
    policy_id: str
    description: str
    evaluate: Callable[[dict], bool]
    severity: str = "deny"  # deny / warn / allow

class PolicyEngine:
    def __init__(self):
        self._policies: List[Policy] = []

    def add(self, policy: Policy) -> None:
        self._policies.append(policy)

    def evaluate(self, context: dict) -> Dict[str, list]:
        denied, warnings = [], []
        for p in self._policies:
            try:
                result = p.evaluate(context)
            except Exception:
                result = False
            if not result:
                if p.severity == "deny":
                    denied.append(p.policy_id)
                else:
                    warnings.append(p.policy_id)
        return {"denied": denied, "warnings": warnings, "allowed": len(denied) == 0}
