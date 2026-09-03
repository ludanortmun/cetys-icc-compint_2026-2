# For the purposes of this activity, a Board is always a 3x3 grid of integers (a tuple of tuples), with the blank tile represented as 0.
# Tuples are immutable and hashable, which makes them suitable for use as dictionary keys or set members, allowing for efficient state tracking during search algorithms.
Board = tuple[tuple[int, ...], ...]

SIZE = 3
BLANK = 0


def from_rows(rows: list[list[int]]) -> Board:
    """Builds a Board from a list of lists. Provided for convenience."""
    return tuple(tuple(row) for row in rows)


def get_position(board: Board, value: int) -> tuple[int, int]:
    """
    Returns the (row, col) position of the given tile value. Raises
    ValueError if the value is not present on the board.
    """
    raise NotImplementedError()


def get_neighboring_states(board: Board) -> list[Board]:
    """
    Returns the Board states reachable from the given one by a single slide
    of a tile adjacent to the blank space (equivalently, by moving the
    blank up, down, left, or right).

    Only moves that keep the blank within the board are valid; there is no
    required order for the returned states. Must not mutate board: each
    neighboring state should be built as its own new Board.
    """
    raise NotImplementedError()


def board_to_str(board: Board) -> str:
    """Returns a human-readable, multi-line rendering of the board."""
    return "\n".join(
        " ".join(str(tile) if tile != BLANK else "." for tile in row) for row in board
    )
