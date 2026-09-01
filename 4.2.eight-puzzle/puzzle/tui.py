"""
Terminal interface for playing back PuzzleSolver's solutions and for
manually exploring get_neighboring_states().
"""
from collections.abc import Callable

from puzzle.puzzles import GOAL_STATE
from puzzle.solver import PuzzleSolver
from puzzle.state import Puzzle

InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], object]

_DIRECTIONS = {
    (-1, 0): "Up",
    (1, 0): "Down",
    (0, -1): "Left",
    (0, 1): "Right",
}


def clear_console() -> None:
    """Clear the terminal and move the cursor to the upper-left corner."""
    print("\033[2J\033[H", end="", flush=True)


def _move_label(current: Puzzle, neighbor: Puzzle) -> str:
    """Describes a neighboring state by which direction the blank moved in."""
    current_blank = current.get_blank_position()
    neighbor_blank = neighbor.get_blank_position()
    delta = (
        neighbor_blank[0] - current_blank[0],
        neighbor_blank[1] - current_blank[1],
    )
    return _DIRECTIONS.get(delta, "?")


def interactive_play(
    start: Puzzle,
    goal: Puzzle = GOAL_STATE,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> None:
    """
    Lets the user manually navigate the puzzle's state graph one move at a
    time, using Puzzle.get_neighboring_states() to list the available
    moves at each step. Useful for manually verifying that method's
    behavior.
    """
    current = start
    moves = 0
    while True:
        output_fn(str(current))
        output_fn("")
        if current == goal:
            output_fn(f"Solved in {moves} moves!")
            return

        neighbors = current.get_neighboring_states()
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
    start: Puzzle,
    goal: Puzzle = GOAL_STATE,
    solver: PuzzleSolver | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> None:
    """
    Solves the puzzle using PuzzleSolver and steps through the resulting
    solution one state at a time, pausing between moves so it can be
    watched move by move.
    """
    solver = solver if solver is not None else PuzzleSolver()
    solution = solver.solve(start, goal)

    output_fn(f"Solution found in {len(solution) - 1} moves.\n")
    for step, state in enumerate(solution):
        output_fn(f"Step {step}/{len(solution) - 1}")
        output_fn(str(state))
        if state != solution[-1]:
            input_fn("Press Enter for the next move...")
        output_fn("")
