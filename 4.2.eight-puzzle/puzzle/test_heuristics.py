"""
Unit tests for manhattan_distance_heuristic() (Part 2).
"""
from puzzle.heuristics import manhattan_distance_heuristic
from puzzle.puzzles import GOAL_STATE
from puzzle.state import Puzzle


class TestManhattanDistanceHeuristic:
    def test_goal_state_has_zero_distance_to_itself(self):
        assert manhattan_distance_heuristic(GOAL_STATE, GOAL_STATE) == 0

    def test_single_slide_has_distance_one(self):
        state = Puzzle.from_rows(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 0, 8],
            ]
        )
        assert manhattan_distance_heuristic(state, GOAL_STATE) == 1

    def test_sums_manhattan_distances_of_all_displaced_tiles(self):
        # Tile 1 is at (0, 2) instead of (0, 0): distance 2.
        # Tile 3 is at (0, 0) instead of (0, 2): distance 2.
        # Every other tile is already in its goal position.
        state = Puzzle.from_rows(
            [
                [3, 2, 1],
                [4, 5, 6],
                [7, 8, 0],
            ]
        )
        assert manhattan_distance_heuristic(state, GOAL_STATE) == 4

    def test_heuristic_matches_the_known_optimal_move_count(self):
        # This board is exactly 2 moves away from GOAL_STATE.
        state = Puzzle.from_rows(
            [
                [1, 2, 3],
                [4, 0, 6],
                [7, 5, 8],
            ]
        )
        assert manhattan_distance_heuristic(state, GOAL_STATE) == 2

    def test_distance_is_symmetric(self):
        state = Puzzle.from_rows(
            [
                [1, 2, 3],
                [4, 0, 6],
                [7, 5, 8],
            ]
        )
        assert manhattan_distance_heuristic(state, GOAL_STATE) == (
            manhattan_distance_heuristic(GOAL_STATE, state)
        )
