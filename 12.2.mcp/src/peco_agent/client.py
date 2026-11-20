"""Student work: connection, discovery, and execution through FastMCP."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastmcp import Client


@asynccontextmanager
async def open_peco(server: Path) -> AsyncIterator[Client]:
    """Open one stdio session using the current Python; close it on context exit."""
    raise NotImplementedError
    yield  # Keep this an async generator until implemented.


async def discover_tools(mcp: Client) -> list[dict[str, Any]]:
    """Discover tools and adapt name, description, input_schema for Chat Completions."""
    raise NotImplementedError


async def execute_tool(mcp: Client, call: Any) -> dict[str, str]:
    """Decode arguments, call MCP, return a tool message with result or error JSON."""
    raise NotImplementedError
