import pytest

from puzzle.puzzle import from_rows, get_position

BOARD = from_rows(
    [
        [1, 2, 3],
        [4, 0, 5],
        [6, 7, 8],
    ]
)


class TestFindsEveryTile:
    @pytest.mark.parametrize(
        "value, expected",
        [
            (1, (0, 0)),
            (2, (0, 1)),
            (3, (0, 2)),
            (4, (1, 0)),
            (0, (1, 1)),
            (5, (1, 2)),
            (6, (2, 0)),
            (7, (2, 1)),
            (8, (2, 2)),
        ],
    )
    def test_returns_row_and_col_of_the_given_value(
        self, value: int, expected: tuple[int, int]
    ):
        assert get_position(BOARD, value) == expected


class TestBlankInDifferentPositions:
    def test_finds_blank_in_top_left_corner(self):
        board = from_rows(
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
            ]
        )
        assert get_position(board, 0) == (0, 0)

    def test_finds_blank_in_bottom_right_corner(self):
        board = from_rows(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0],
            ]
        )
        assert get_position(board, 0) == (2, 2)


class TestMissingValue:
    def test_raises_value_error_when_the_value_is_not_on_the_board(self):
        with pytest.raises(ValueError):
            _ = get_position(BOARD, 9)
