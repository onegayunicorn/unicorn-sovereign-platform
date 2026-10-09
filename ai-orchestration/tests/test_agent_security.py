"""Agent security rule tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from agents.registry import AgentRegistry, AgentSpec, RiskLevel
from agents.runtime import AgentRuntime
from tools.registry import ToolRegistry, ToolSpec
from tools.permissions import PermissionEnforcer, PermissionDenied

def test_no_shell_execution():
    reg = AgentRegistry()
    reg.register(AgentSpec(agent_id="a1", name="test", purpose="test", allowed_tools=["shell"]))
    rt = AgentRuntime(reg)
    result = rt.execute("a1", "run", tool="shell")
    assert result["status"] == "rejected"

def test_kill_switch():
    reg = AgentRegistry()
    reg.register(AgentSpec(agent_id="a1", name="test", purpose="test"))
    rt = AgentRuntime(reg)
    rt.kill_switch.trigger("agent", "a1")
    result = rt.execute("a1", "read")
    assert result["status"] == "killed"

def test_agents_cannot_modify_permissions():
    treg = ToolRegistry()
    treg.register(ToolSpec(tool_id="modify_permissions", name="mod", description="mod"))
    enforcer = PermissionEnforcer(treg)
    agent = AgentSpec(agent_id="a1", name="test", purpose="test", allowed_tools=["modify_permissions"])
    assert not enforcer.check(agent, "modify_permissions")
