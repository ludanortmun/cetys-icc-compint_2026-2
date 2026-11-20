import pytest
from fastmcp.exceptions import ToolError
from conftest import todo


@pytest.mark.parametrize("changes", [
    {"content": "New title with spaces"}, {"due": "2026-12-03"},
    {"content": "Updated title", "due": "2026-12-04"},
])
async def test_edit_preserves_other_fields(mcp, peco_env, changes):
    original = todo(state="done")
    peco_env.seed([original, todo(9, "Other task")])
    result = await mcp.call_tool("edit_todo", {"todo_id": 7, **changes})
    assert "Updated todo 7" in result.data
    assert peco_env.read() == [{**original, **changes}, todo(9, "Other task")]


async def test_missing_id(mcp, peco_env):
    with pytest.raises(ToolError):
        await mcp.call_tool("edit_todo", {"todo_id": 999, "content": "Missing"})
    assert peco_env.read() == []
