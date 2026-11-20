from types import SimpleNamespace
from unittest.mock import AsyncMock
from peco_agent.client import discover_tools


async def test_dynamic_schema_adaptation():
    schema = {"type": "object", "properties": {"value": {"type": "integer"}}, "required": ["value"]}
    client = SimpleNamespace(list_tools=AsyncMock(return_value=[
        SimpleNamespace(name="list_todos", description="List peco TODOs", input_schema=schema),
        SimpleNamespace(name="complete_todo", description=None, input_schema={"type": "object"}),
    ]))
    assert await discover_tools(client) == [
        {"type": "function", "function": {"name": "list_todos", "description": "List peco TODOs", "parameters": schema}},
        {"type": "function", "function": {"name": "complete_todo", "description": "", "parameters": {"type": "object"}}},
    ]
    client.list_tools.assert_awaited_once()


async def test_no_tools():
    client = SimpleNamespace(list_tools=AsyncMock(return_value=[]))
    assert await discover_tools(client) == []
