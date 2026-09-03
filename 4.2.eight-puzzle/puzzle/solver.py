import heapq
from collections.abc import Callable
from math import inf

from puzzle.heuristics import manhattan_distance_heuristic
from puzzle.puzzle import Board, get_neighboring_states

HeuristicFn = Callable[[Board, Board], float]


def solve(
    start: Board,
    goal: Board,
    heuristic: HeuristicFn = manhattan_distance_heuristic,
) -> list[Board] | None:
    """
    Runs A* from start to goal. Every move has a cost of 1, and heuristic
    estimates the remaining cost from a state to goal. You may assume goal
    is always reachable from start.

    Returns the sequence of Board states from start to goal, both
    inclusive, representing an optimal (fewest-moves) solution.
    """
    raise NotImplementedError()
