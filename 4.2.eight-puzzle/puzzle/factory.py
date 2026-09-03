import random

from puzzle.puzzle import BLANK, Board, from_rows, get_neighboring_states

GOAL_STATE = from_rows(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, BLANK],
    ]
)

EASY_START = from_rows(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, BLANK, 8],
    ]
)

MEDIUM_START = from_rows(
    [
        [1, 2, 3],
        [BLANK, 4, 6],
        [7, 5, 8],
    ]
)

HARD_START = from_rows(
    [
        [8, 6, 7],
        [2, 5, 4],
        [3, BLANK, 1],
    ]
)


def random_puzzle(moves: int = 30, seed: int | None = None) -> Board:
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
            for neighbor in get_neighboring_states(state)
            if neighbor != previous
        ]
        previous = state
        state = rng.choice(candidates or get_neighboring_states(state))
    return state
