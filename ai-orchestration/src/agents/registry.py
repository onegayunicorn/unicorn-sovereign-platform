"""Agent registry — purpose, tools, risk level."""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentSpec(BaseModel):
    agent_id: str
    name: str
    purpose: str
    allowed_tools: List[str] = Field(default_factory=list)
    risk_level: RiskLevel = RiskLevel.LOW
    tenant_id: Optional[str] = None
    enabled: bool = True
    max_concurrency: int = 1

class AgentRegistry:
    def __init__(self):
        self._agents: dict[str, AgentSpec] = {}

    def register(self, spec: AgentSpec) -> None:
        if spec.agent_id in self._agents:
            raise ValueError(f"Agent {spec.agent_id} already registered")
        self._agents[spec.agent_id] = spec

    def get(self, agent_id: str) -> AgentSpec | None:
        return self._agents.get(agent_id)

    def list_enabled(self) -> List[AgentSpec]:
        return [a for a in self._agents.values() if a.enabled]
