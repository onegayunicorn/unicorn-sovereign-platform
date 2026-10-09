"""Tool permission enforcement for NPCs."""
from __future__ import annotations
from .registry import NPCToolRegistry, FORBIDDEN_TOOL_CATEGORIES

class NPCPermissionEnforcer:
    def __init__(self, registry: NPCToolRegistry):
        self.registry = registry

    def allow(self, tool_id: str) -> bool:
        tool = self.registry._tools.get(tool_id)
        if not tool:
            return False
        return tool.category not in FORBIDDEN_TOOL_CATEGORIES
