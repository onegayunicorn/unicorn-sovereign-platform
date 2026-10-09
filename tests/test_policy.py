import pytest
from ai_orchestration.src.tools.permissions import authorize, PermissionDenied
from ai_orchestration.src.tools.registry import ToolSpec
def test_external_action_requires_human_approval():
    tool = ToolSpec("publish", "publish", external=True)
    with pytest.raises(PermissionDenied): authorize(tool, {"publish"})
    authorize(tool, {"publish"}, human_approved=True)
