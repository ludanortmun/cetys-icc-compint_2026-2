import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

from fastmcp.exceptions import ToolError
from openai.types.chat import ChatCompletionMessage
import pytest

from conftest import Model
from peco_agent.client import execute_tool
from peco_agent.chat import reply


def call(identifier, name="list_todos", arguments="{}"):
    return {"id": identifier, "type": "function", "function": {"name": name, "arguments": arguments}}


async def test_results_multiple_calls_and_rounds():
    first = ChatCompletionMessage(role="assistant", tool_calls=[
        call("a"), call("b", "create_todo", '{"content":"Read"}')])
    second = ChatCompletionMessage(role="assistant", tool_calls=[call("c", arguments='{"include_done":true}')])
    model = Model(first, second, ChatCompletionMessage(role="assistant", content="Saved."),
                  ChatCompletionMessage(role="assistant", content="You asked to read."))
    client = SimpleNamespace(call_tool=AsyncMock(side_effect=[
        SimpleNamespace(data="ID STATE DUE CONTENT"), SimpleNamespace(data="Created todo 1"),
        SimpleNamespace(data="1 pending - Read")]))
    history = [{"role": "user", "content": "Add Read and list tasks"}]
    assert await reply(model, client, [], history, "test-model") == "Saved."
    client.call_tool.assert_any_await("create_todo", {"content": "Read"})
    client.call_tool.assert_any_await("list_todos", {"include_done": True})
    results = [m for m in history if m["role"] == "tool"]
    assert [m["tool_call_id"] for m in results] == ["a", "b", "c"]
    assert [json.loads(m["content"]) for m in results] == [
        {"result": "ID STATE DUE CONTENT"}, {"result": "Created todo 1"}, {"result": "1 pending - Read"}]
    assert [m["role"] for m in history] == ["user", "assistant", "tool", "tool", "assistant", "tool", "assistant"]
    assert len(model.requests[1]["messages"]) == 4
    history.append({"role": "user", "content": "What did I ask?"})
    assert await reply(model, client, [], history, "test-model") == "You asked to read."
    assert len(model.requests[-1]["messages"]) == 8


@pytest.mark.parametrize("arguments, failure", [("not json", None), ('{"todo_id":999}', ToolError("todo not found"))])
async def test_error_is_returned_to_model(arguments, failure):
    request = ChatCompletionMessage(role="assistant", tool_calls=[call("bad", "complete_todo", arguments)]).tool_calls[0]
    client = SimpleNamespace(call_tool=AsyncMock(side_effect=failure))
    result = await execute_tool(client, request)
    assert result["role"] == "tool" and result["tool_call_id"] == "bad"
    payload = json.loads(result["content"])
    assert isinstance(payload.get("error"), str) and payload["error"]
    assert "result" not in payload
    if failure is None:
        client.call_tool.assert_not_awaited()


async def test_real_mcp_result(mcp):
    request = ChatCompletionMessage(role="assistant", tool_calls=[call("real")]).tool_calls[0]
    result = await execute_tool(mcp, request)
    assert "ID" in json.loads(result["content"])["result"]
