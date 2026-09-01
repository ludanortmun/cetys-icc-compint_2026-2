import math


def manhattan_distance(node: tuple[int, int], target: tuple[int, int]) -> float:
    """
    Returns the Manhattan (taxicab) distance between node and target.

    This is the exact remaining cost for grids where movement is restricted
    to 4 directions (up, down, left, right) and every step costs 1.
    """
    raise NotImplementedError()


def euclidean_distance(node: tuple[int, int], target: tuple[int, int]) -> float:
    """
    Returns the Euclidean (straight-line) distance between node and target.

    This is appropriate for grids where movement is allowed in 8 directions
    and a diagonal step costs its true geometric length, sqrt(2).
    """
    raise NotImplementedError()


def chebyshev_distance(node: tuple[int, int], target: tuple[int, int]) -> float:
    """
    Returns the Chebyshev distance between node and target.

    This is the exact remaining cost for grids where movement is allowed in
    8 directions and every step, orthogonal or diagonal, costs 1.
    """
    raise NotImplementedError()
