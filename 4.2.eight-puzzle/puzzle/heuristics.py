from puzzle.puzzle import BLANK, Board, get_position


def manhattan_distance_heuristic(state: Board, goal: Board) -> int:
    """
    Returns the sum, over every non-blank tile, of the Manhattan distance
    between that tile's position in state and its position in goal.
    """
    raise NotImplementedError()
