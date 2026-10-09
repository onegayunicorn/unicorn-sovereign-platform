"""Allowed tool registry — NPC tools have NO shell, file, or network access."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

FORBIDDEN_TOOL_CATEGORIES = {"shell", "file_access", "network", "subprocess", "exec"}

@dataclass
class NPCTool:
    tool_id: str
    name: str
    category: str  # must not be in FORBIDDEN_TOOL_CATEGORIES
    description: str

class NPCToolRegistry:
    def __init__(self):
        self._tools: Dict[str, NPCTool] = {}

    def register(self, tool: NPCTool) -> bool:
        if tool.category in FORBIDDEN_TOOL_CATEGORIES:
            return False
        self._tools[tool.tool_id] = tool
        return True

    def list_tools(self) -> List[NPCTool]:
        return list(self._tools.values())
