"""Student work: discovery and execution through FastMCP."""

from typing import Any

from fastmcp import Client


async def discover_tools(mcp: Client) -> list[dict[str, Any]]:
    """Discover tools and adapt name, description, input_schema for Chat Completions."""
    raise NotImplementedError


async def execute_tool(mcp: Client, call: Any) -> dict[str, str]:
    """Decode arguments, call MCP, and return a Chat Completions tool message.

    Example: {"role": "tool", "tool_call_id": call.id, "content": '{"result": "Created todo 1"}'}.
    The content must be a JSON string containing either the result or an error.
    """
    raise NotImplementedError
