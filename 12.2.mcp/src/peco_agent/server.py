"""Implement the four tools using the peco CLI. Keep stdout for MCP."""

from fastmcp import FastMCP

mcp = FastMCP("peco")


@mcp.tool
def list_todos(include_done: bool = False) -> str:
    """List peco TODOs with IDs, state, due dates and content; optionally include done."""
    raise NotImplementedError


@mcp.tool
def create_todo(content: str, due: str | None = None) -> str:
    """Create a pending TODO. Optional due date uses local YYYY-MM-DD."""
    raise NotImplementedError


@mcp.tool
def edit_todo(todo_id: int, content: str | None = None, due: str | None = None) -> str:
    """Edit an existing TODO by ID, preserving fields whose arguments are None."""
    raise NotImplementedError


@mcp.tool
def complete_todo(todo_id: int) -> str:
    """Mark an existing TODO as done using its peco ID."""
    raise NotImplementedError


if __name__ == "__main__":
    mcp.run(transport="stdio")
