"""
Distance heuristics for grid-based pathfinding.

Each function estimates the remaining cost between two grid coordinates,
expressed as (x, y) tuples. They are used to guide informed search
algorithms such as A*, which combine the real accumulated cost g(n) with an
estimate h(n) of the remaining cost to the target.
"""
import math


def manhattan_distance(node: tuple[int, int], target: tuple[int, int]) -> float:
    """
    Returns the Manhattan (taxicab) distance between node and target:

        h(n) = |x_n - x_target| + |y_n - y_target|

    This is the exact remaining cost for grids where movement is restricted
    to 4 directions (up, down, left, right) and every step costs 1.
    """
    raise NotImplementedError()


def euclidean_distance(node: tuple[int, int], target: tuple[int, int]) -> float:
    """
    Returns the Euclidean (straight-line) distance between node and target:

        h(n) = sqrt((x_n - x_target)^2 + (y_n - y_target)^2)

    This is appropriate for grids where movement is allowed in 8 directions
    and a diagonal step costs its true geometric length, sqrt(2).
    """
    raise NotImplementedError()


def chebyshev_distance(node: tuple[int, int], target: tuple[int, int]) -> float:
    """
    Returns the Chebyshev distance between node and target:

        h(n) = max(|x_n - x_target|, |y_n - y_target|)

    This is the exact remaining cost for grids where movement is allowed in
    8 directions and every step, orthogonal or diagonal, costs 1.
    """
    raise NotImplementedError()
