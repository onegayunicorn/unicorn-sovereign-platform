"""Tool permission enforcement."""
from __future__ import annotations
from .registry import ToolRegistry, ToolSpec
from ..agents.registry import AgentSpec

class PermissionDenied(Exception):
    pass

class PermissionEnforcer:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    def check(self, agent: AgentSpec, tool_id: str) -> bool:
        tool = self.tool_registry.get(tool_id)
        if not tool:
            return False
        if tool.allowed_agents and agent.agent_id not in tool.allowed_agents:
            return False
        if tool_id not in agent.allowed_tools:
            return False
        # Hardcoded: agents cannot modify their own permissions
        if tool_id == "modify_permissions":
            return False
        return True

    def enforce(self, agent: AgentSpec, tool_id: str) -> None:
        if not self.check(agent, tool_id):
            raise PermissionDenied(f"Agent {agent.agent_id} denied tool {tool_id}")
