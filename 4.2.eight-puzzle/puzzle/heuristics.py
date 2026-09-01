"""
Heuristic used to guide PuzzleSolver's A* search.

The sum of Manhattan distances of every tile from its position in a state
to its position in the goal is an admissible, informative heuristic for the
8-puzzle: any single slide can move exactly one tile one step closer to (or
farther from) its goal position, so the true remaining cost can never be
smaller than this sum.
"""
from puzzle.state import BLANK, Puzzle


def manhattan_distance_heuristic(state: Puzzle, goal: Puzzle) -> int:
    """
    Returns the sum, over every non-blank tile, of the Manhattan distance
    between that tile's position in state and its position in goal.
    """
    raise NotImplementedError()
