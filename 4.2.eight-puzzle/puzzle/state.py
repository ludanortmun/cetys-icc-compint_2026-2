"""
Representation of an 8-puzzle state as an immutable 3x3 board.

The blank tile is represented as 0. Boards are stored as a tuple of tuples,
which makes Puzzle instances hashable and comparable with `==`, so they can
be used directly as dictionary keys or set members (e.g. a `visited` set
during search) without any extra bookkeeping.

The full state graph of an 8-puzzle has 9!/2 = 181,440 reachable states, so
it is never built up front. Instead, get_neighboring_states() computes a
state's neighbors on demand: the graph is discovered lazily, one state at a
time, as a search algorithm actually needs it.
"""
from dataclasses import dataclass

Board = tuple[tuple[int, ...], ...]

SIZE = 3
BLANK = 0


@dataclass(frozen=True)
class Puzzle:
    board: Board

    def __post_init__(self) -> None:
        if len(self.board) != SIZE or any(len(row) != SIZE for row in self.board):
            raise ValueError(f"board must be a {SIZE}x{SIZE} matrix")

    def get_blank_position(self) -> tuple[int, int]:
        """Returns the (row, col) position of the blank tile (0)."""
        for row in range(SIZE):
            for col in range(SIZE):
                if self.board[row][col] == BLANK:
                    return row, col
        raise ValueError("board has no blank tile")

    def get_neighboring_states(self) -> list["Puzzle"]:
        """
        Returns the Puzzle states reachable from this one by a single slide
        of a tile adjacent to the blank space (equivalently, by moving the
        blank up, down, left, or right).

        Only moves that keep the blank within the board are valid; there is
        no required order for the returned states. Must not mutate
        self.board: each neighboring state should be built as its own new
        Puzzle instance.
        """
        raise NotImplementedError()

    @classmethod
    def from_rows(cls, rows: list[list[int]]) -> "Puzzle":
        """Builds a Puzzle from a list of lists. Provided for convenience."""
        return cls(tuple(tuple(row) for row in rows))

    def __str__(self) -> str:
        return "\n".join(
            " ".join(str(tile) if tile != BLANK else "." for tile in row)
            for row in self.board
        )
