"""Unauthorized tool access tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages"))
from npc_core.tools.registry import NPCToolRegistry, NPCTool, FORBIDDEN_TOOL_CATEGORIES
from npc_core.tools.permissions import NPCPermissionEnforcer

def test_shell_tool_rejected():
    reg = NPCToolRegistry()
    result = reg.register(NPCTool("shell", "Shell", "shell", "run commands"))
    assert result is False

def test_safe_tool_accepted():
    reg = NPCToolRegistry()
    result = reg.register(NPCTool("dialogue", "Dialogue", "dialogue", "talk"))
    assert result is True
    enforcer = NPCPermissionEnforcer(reg)
    assert enforcer.allow("dialogue")
    assert not enforcer.allow("nonexistent")
