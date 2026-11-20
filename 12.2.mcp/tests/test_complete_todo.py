import pytest
from fastmcp.exceptions import ToolError
from conftest import todo


async def test_complete_only_requested_task(mcp, peco_env):
    peco_env.seed([todo(), todo(9, "Keep pending")])
    result = await mcp.call_tool("complete_todo", {"todo_id": 7})
    assert "Completed todo 7" in result.data
    assert peco_env.read() == [todo(state="done"), todo(9, "Keep pending")]


async def test_missing_id(mcp, peco_env):
    with pytest.raises(ToolError):
        await mcp.call_tool("complete_todo", {"todo_id": 999})
    assert peco_env.read() == []
