"""
Sample puzzles and a random-puzzle generator used by the TUI. You do not
need to modify anything in this file.
"""
import random

from puzzle.state import BLANK, Puzzle

GOAL_STATE = Puzzle.from_rows(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, BLANK],
    ]
)

EASY_START = Puzzle.from_rows(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, BLANK, 8],
    ]
)

MEDIUM_START = Puzzle.from_rows(
    [
        [1, 2, 3],
        [BLANK, 4, 6],
        [7, 5, 8],
    ]
)

HARD_START = Puzzle.from_rows(
    [
        [8, 6, 7],
        [2, 5, 4],
        [3, BLANK, 1],
    ]
)


def random_puzzle(moves: int = 30, seed: int | None = None) -> Puzzle:
    """
    Returns a puzzle obtained by taking a random walk of the given number
    of moves starting from GOAL_STATE. Walking away from a known-solvable
    state (rather than shuffling tiles directly) guarantees the result is
    always solvable, since every move it makes is reversible.
    """
    rng = random.Random(seed)
    state = GOAL_STATE
    previous = None
    for _ in range(moves):
        candidates = [
            neighbor
            for neighbor in state.get_neighboring_states()
            if neighbor != previous
        ]
        previous = state
        state = rng.choice(candidates or state.get_neighboring_states())
    return state
