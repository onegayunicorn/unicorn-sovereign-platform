"""Agent execution runtime with kill-switch support."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from .registry import AgentRegistry, AgentSpec

@dataclass
class KillSwitch:
    """Kill switches: per-tenant, per-agent, per-tool, per-provider."""
    tenant: Dict[str, bool] = field(default_factory=dict)
    agent: Dict[str, bool] = field(default_factory=dict)
    tool: Dict[str, bool] = field(default_factory=dict)
    provider: Dict[str, bool] = field(default_factory=dict)

    def is_blocked(self, tenant: str | None, agent: str, tool: str | None, provider: str | None) -> bool:
        return (self.tenant.get(tenant, False) or self.agent.get(agent, False)
                or self.tool.get(tool, False) or self.provider.get(provider, False))

    def trigger(self, scope: str, key: str) -> None:
        getattr(self, scope)[key] = True

class AgentRuntime:
    def __init__(self, registry: AgentRegistry):
        self.registry = registry
        self.kill_switch = KillSwitch()
        self._approvals_pending: list[dict] = []

    def execute(self, agent_id: str, action: str, tool: str | None = None,
                provider: str | None = None, tenant: str | None = None) -> dict:
        spec = self.registry.get(agent_id)
        if not spec or not spec.enabled:
            return {"status": "rejected", "reason": "agent not found or disabled"}
        if self.kill_switch.is_blocked(tenant, agent_id, tool, provider):
            return {"status": "killed", "reason": "kill switch active"}
        # Hardcoded rule: no arbitrary shell execution
        if tool in ("shell", "bash", "exec", "subprocess"):
            return {"status": "rejected", "reason": "arbitrary shell execution forbidden"}
        # Hardcoded rule: destructive/financial/external actions require human approval
        if action in ("delete", "transfer_funds", "exfiltrate", "send_external"):
            approval = {"agent_id": agent_id, "action": action, "tool": tool, "status": "pending"}
            self._approvals_pending.append(approval)
            return {"status": "approval_required", "approval": approval}
        return {"status": "executed", "agent_id": agent_id, "action": action}
