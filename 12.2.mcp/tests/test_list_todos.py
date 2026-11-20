from conftest import todo


async def test_pending_and_completed(mcp, peco_env):
    peco_env.seed([todo(), todo(8, "Already finished", None, "done")])
    result = await mcp.call_tool("list_todos", {})
    assert "Read chapter" in result.data and "2026-12-01" in result.data
    assert "7" in result.data and "pending" in result.data
    assert "Already finished" not in result.data
    result = await mcp.call_tool("list_todos", {"include_done": True})
    assert "Already finished" in result.data and "done" in result.data
    assert peco_env.calls() == [["list"], ["list", "--include-done"]]


async def test_empty(mcp, peco_env):
    result = await mcp.call_tool("list_todos", {})
    assert isinstance(result.data, str) and "ID" in result.data
    assert peco_env.calls() == [["list"]]
