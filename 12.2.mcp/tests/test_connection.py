import pytest
from conftest import SERVER
from peco_agent.client import open_peco


async def test_stdio_session_lifecycle(peco_env):
    async with open_peco(SERVER) as client:
        assert client.is_connected()
        tools = await client.list_tools()
        assert {t.name for t in tools} == {
            "list_todos", "create_todo", "edit_todo", "complete_todo"}
    assert not client.is_connected()


async def test_close_on_exception(peco_env):
    with pytest.raises(RuntimeError, match="leave session"):
        async with open_peco(SERVER) as client:
            assert client.is_connected()
            raise RuntimeError("leave session")
    assert not client.is_connected()
