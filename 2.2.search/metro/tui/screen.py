"""Small terminal-screen helpers shared by the metro TUI."""

from __future__ import annotations

from collections.abc import Callable


InputFunction = Callable[[str], str]


def clear_console() -> None:
    """Clear the terminal and move the cursor to the upper-left corner."""
    print("\033[2J\033[H", end="", flush=True)


def wait_for_main_menu(input_fn: InputFunction) -> None:
    """Keep a completed flow visible until the rider returns to the main menu."""
    input_fn("Press Enter to return to the main menu...")
