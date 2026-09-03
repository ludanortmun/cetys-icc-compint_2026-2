from puzzle.puzzle import from_rows, get_neighboring_states


class TestBlankInCorner:
    def test_top_left_blank_has_two_neighbors(self):
        board = from_rows(
            [
                [0, 1, 2],
                [3, 4, 5],
                [6, 7, 8],
            ]
        )
        neighbors = get_neighboring_states(board)

        assert len(neighbors) == 2
        assert set(neighbors) == {
            ((1, 0, 2), (3, 4, 5), (6, 7, 8)),
            ((3, 1, 2), (0, 4, 5), (6, 7, 8)),
        }

    def test_bottom_right_blank_has_two_neighbors(self):
        board = from_rows(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0],
            ]
        )
        neighbors = get_neighboring_states(board)

        assert len(neighbors) == 2
        assert set(neighbors) == {
            ((1, 2, 3), (4, 5, 6), (7, 0, 8)),
            ((1, 2, 3), (4, 5, 0), (7, 8, 6)),
        }


class TestBlankOnEdge:
    def test_top_edge_blank_has_three_neighbors(self):
        board = from_rows(
            [
                [1, 0, 2],
                [3, 4, 5],
                [6, 7, 8],
            ]
        )
        neighbors = get_neighboring_states(board)

        assert len(neighbors) == 3
        assert set(neighbors) == {
            ((0, 1, 2), (3, 4, 5), (6, 7, 8)),
            ((1, 2, 0), (3, 4, 5), (6, 7, 8)),
            ((1, 4, 2), (3, 0, 5), (6, 7, 8)),
        }

    def test_left_edge_blank_has_three_neighbors(self):
        board = from_rows(
            [
                [1, 2, 3],
                [0, 4, 5],
                [6, 7, 8],
            ]
        )
        neighbors = get_neighboring_states(board)

        assert len(neighbors) == 3
        assert set(neighbors) == {
            ((0, 2, 3), (1, 4, 5), (6, 7, 8)),
            ((1, 2, 3), (4, 0, 5), (6, 7, 8)),
            ((1, 2, 3), (6, 4, 5), (0, 7, 8)),
        }


class TestBlankInCenter:
    def test_center_blank_has_four_neighbors(self):
        board = from_rows(
            [
                [1, 2, 3],
                [4, 0, 5],
                [6, 7, 8],
            ]
        )
        neighbors = get_neighboring_states(board)

        assert len(neighbors) == 4
        assert set(neighbors) == {
            ((1, 0, 3), (4, 2, 5), (6, 7, 8)),
            ((1, 2, 3), (4, 7, 5), (6, 0, 8)),
            ((1, 2, 3), (0, 4, 5), (6, 7, 8)),
            ((1, 2, 3), (4, 5, 0), (6, 7, 8)),
        }


class TestDoesNotMutateOriginal:
    def test_original_board_is_unchanged_after_computing_neighbors(self):
        board = from_rows([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

        _ = get_neighboring_states(board)

        assert board == ((1, 2, 3), (4, 0, 5), (6, 7, 8))


class TestReturnsBoardInstances:
    def test_neighbors_are_tuples(self):
        board = from_rows([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

        for neighbor in get_neighboring_states(board):
            assert isinstance(neighbor, tuple)

    def test_neighbors_only_differ_by_swapping_the_blank_with_one_tile(self):
        board = from_rows([[1, 2, 3], [4, 0, 5], [6, 7, 8]])

        for neighbor in get_neighboring_states(board):
            differences = [
                (r, c)
                for r in range(3)
                for c in range(3)
                if board[r][c] != neighbor[r][c]
            ]
            assert len(differences) == 2
