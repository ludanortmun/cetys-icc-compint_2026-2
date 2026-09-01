"""
Unit tests for Puzzle.get_neighboring_states() (Part 1).

These only exercise the lazy generation of neighboring puzzle states from a
given board; they do not depend on the heuristic or the solver.
"""
from puzzle.state import Puzzle


def _boards(states):
    return {state.board for state in states}


class TestBlankInCorner:
    def test_top_left_blank_has_two_neighbors(self):
        puzzle = Puzzle.from_rows(
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
            ]
        )
        neighbors = puzzle.get_neighboring_states()

        assert len(neighbors) == 2
        assert _boards(neighbors) == {
            ((1, 0, 2), (3, 4, 5), (6, 7, 8)),
            ((3, 1, 2), (0, 4, 5), (6, 7, 8)),
        }

    def test_bottom_right_blank_has_two_neighbors(self):
        puzzle = Puzzle.from_rows(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0],
            ]
        )
        neighbors = puzzle.get_neighboring_states()

        assert len(neighbors) == 2
        assert _boards(neighbors) == {
            ((1, 2, 3), (4, 5, 6), (7, 0, 8)),
            ((1, 2, 3), (4, 5, 0), (7, 8, 6)),
        }


class TestBlankOnEdge:
    def test_top_edge_blank_has_three_neighbors(self):
        puzzle = Puzzle.from_rows(
            [
                [1, 0, 2],
                [3, 4, 5],
                [6, 7, 8],
            ]
        )
        neighbors = puzzle.get_neighboring_states()

        assert len(neighbors) == 3
        assert _boards(neighbors) == {
            ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
            ((1, 2, 0), (3, 4, 5), (6, 7, 8)),
            ((1, 4, 2), (3, 0, 5), (6, 7, 8)),
        }

    def test_left_edge_blank_has_three_neighbors(self):
        puzzle = Puzzle.from_rows(
            [
                [1, 2, 3],
                [0, 4, 5],
                [6, 7, 8],
            ]
        )
        neighbors = puzzle.get_neighboring_states()

        assert len(neighbors) == 3
        assert _boards(neighbors) == {
            ((0, 2, 3), (1, 4, 5), (6, 7, 8)),
            ((1, 2, 3), (4, 0, 5), (6, 7, 8)),
            ((1, 2, 3), (6, 4, 5), (0, 7, 8)),
        }


class TestBlankInCenter:
    def test_center_blank_has_four_neighbors(self):
        puzzle = Puzzle.from_rows(
            [
                [1, 2, 3],
                [4, 0, 5],
                [6, 7, 8],
            ]
        )
        neighbors = puzzle.get_neighboring_states()

        assert len(neighbors) == 4
        assert _boards(neighbors) == {
            ((1, 0, 3), (4, 2, 5), (6, 7, 8)),
            ((1, 2, 3), (4, 7, 5), (6, 0, 8)),
            ((1, 2, 3), (0, 4, 5), (6, 7, 8)),
            ((1, 2, 3), (4, 5, 0), (6, 7, 8)),
        }


class TestDoesNotMutateOriginal:
    def test_original_board_is_unchanged_after_computing_neighbors(self):
        puzzle = Puzzle.from_rows([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

        puzzle.get_neighboring_states()

        assert puzzle.board == ((1, 2, 3), (4, 0, 5), (6, 7, 8))


class TestReturnsPuzzleInstances:
    def test_neighbors_are_puzzle_instances(self):
        puzzle = Puzzle.from_rows([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

        for neighbor in puzzle.get_neighboring_states():
            assert isinstance(neighbor, Puzzle)

    def test_neighbors_only_differ_by_swapping_the_blank_with_one_tile(self):
        puzzle = Puzzle.from_rows([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

        for neighbor in puzzle.get_neighboring_states():
            differences = [
                (r, c)
                for r in range(3)
                for c in range(3)
                if puzzle.board[r][c] != neighbor.board[r][c]
            ]
            assert len(differences) == 2
