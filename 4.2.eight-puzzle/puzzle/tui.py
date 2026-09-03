from collections.abc import Callable

from puzzle.factory import GOAL_STATE
from puzzle.puzzle import (
    BLANK,
    Board,
    board_to_str,
    get_neighboring_states,
    get_position,
)
from puzzle.solver import HeuristicFn, solve

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]

_DIRECTIONS = {
    (-1, 0): "Up",
    (1, 0): "Down",
    (0, -1): "Left",
    (0, 1): "Right",
}


def clear_console() -> None:
    """Clear the terminal and move the cursor to the upper-left corner."""
    print("\033[2J\033[H", end="", flush=True)


def _move_label(current: Board, neighbor: Board) -> str:
    """Describes a neighboring state by which direction the blank moved in."""
    current_blank = get_position(current, BLANK)
    neighbor_blank = get_position(neighbor, BLANK)
    delta = (
        neighbor_blank[0] - current_blank[0],
        neighbor_blank[1] - current_blank[1],
    )
    return _DIRECTIONS.get(delta, "?")


def interactive_play(
    start: Board,
    goal: Board = GOAL_STATE,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> None:
    """
    Lets the user manually navigate the puzzle's state graph one move at a
    time, using get_neighboring_states() to list the available moves at
    each step. Useful for manually verifying that function's behavior.
    """
    current = start
    moves = 0
    while True:
        output_fn(board_to_str(current))
        output_fn("")
        if current == goal:
            output_fn(f"Solved in {moves} moves!")
            return

        neighbors = get_neighboring_states(current)
        options = [(_move_label(current, neighbor), neighbor) for neighbor in neighbors]
        for index, (label, _) in enumerate(options, start=1):
            output_fn(f"{index}. {label}")
        output_fn("Q. Quit")

        choice = input_fn("Choose a move: ").strip()
        if choice.casefold() == "q":
            return
        if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
            output_fn("Invalid option.\n")
            continue

        current = options[int(choice) - 1][1]
        moves += 1
        output_fn("")


def playback_solution(
    start: Board,
    goal: Board = GOAL_STATE,
    heuristic: HeuristicFn | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> None:
    """
    Solves the puzzle using solve() and steps through the resulting
    solution one state at a time, pausing between moves so it can be
    watched move by move.
    """
    solution = (
        solve(start, goal, heuristic) if heuristic is not None else solve(start, goal)
    )

    if solution is None:
        output_fn("No solution found.\n")
        return

    output_fn(f"Solution found in {len(solution) - 1} moves.\n")
    for step, state in enumerate(solution):
        output_fn(f"Step {step}/{len(solution) - 1}")
        output_fn(board_to_str(state))
        if state != solution[-1]:
            _ = input_fn("Press Enter for the next move...")
        output_fn("")
