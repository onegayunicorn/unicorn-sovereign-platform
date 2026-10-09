"""Tool registry with permission declarations."""
from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional

class ToolSpec(BaseModel):
    tool_id: str
    name: str
    description: str
    requires_approval: bool = False
    risk_category: str = "low"  # low / destructive / financial / external
    allowed_agents: List[str] = []  # empty = all
    network_access: bool = False
    file_access: bool = False

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.tool_id] = spec

    def get(self, tool_id: str) -> Optional[ToolSpec]:
        return self._tools.get(tool_id)
