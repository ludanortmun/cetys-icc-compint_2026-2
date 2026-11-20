import pytest
from fastmcp.exceptions import ToolError


@pytest.mark.parametrize("due", [None, "2026-12-02"])
async def test_create(mcp, peco_env, tmp_path, due):
    marker = tmp_path / "must-not-exist"
    content = f'Buy milk; touch {marker} $(echo unsafe) "quoted"'
    arguments = {"content": content}
    if due is not None:
        arguments["due"] = due
    result = await mcp.call_tool("create_todo", arguments)
    assert "Created todo 1" in result.data
    assert peco_env.read() == [dict(id=1, content=content, due=due, state="pending")]
    assert not marker.exists()


async def test_creation_failure(mcp, peco_env):
    with pytest.raises(ToolError):
        await mcp.call_tool("create_todo", {"content": ""})
    assert peco_env.read() == []
