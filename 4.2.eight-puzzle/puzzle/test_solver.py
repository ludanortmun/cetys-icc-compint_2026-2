"""
Unit tests for solve() (Part 2).

Solution validity and optimality are checked with a small breadth-first
search over get_neighboring_states(), independent of the solver, so these
tests do not assume any particular heuristic implementation, only that the
returned solution is a valid, optimal path from start to goal. All puzzles
used here are solvable; solve() may assume the goal is always reachable
from the start.
"""

from collections import deque

from puzzle.factory import GOAL_STATE
from puzzle.puzzle import Board, from_rows, get_neighboring_states
from puzzle.solver import solve


# Using BFS as a reference optimal path length.
def _bfs_optimal_length(start: Board, goal: Board) -> int | None:
    if start == goal:
        return 0

    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        state, depth = queue.popleft()
        for neighbor in get_neighboring_states(state):
            if neighbor == goal:
                return depth + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, depth + 1))
    return None


def _assert_valid_solution(solution: list[Board], start: Board, goal: Board):
    assert solution[0] == start
    assert solution[-1] == goal
    for current, next_state in zip(solution, solution[1:]):
        assert next_state in get_neighboring_states(current)


ONE_MOVE_AWAY = from_rows(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 0, 8],
    ]
)

TWO_MOVES_AWAY = from_rows(
    [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8],
    ]
)

THREE_MOVES_AWAY = from_rows(
    [
        [1, 2, 3],
        [0, 4, 6],
        [7, 5, 8],
    ]
)


class TestSolvesTrivialPuzzle:
    def test_already_at_goal_returns_single_state_solution(self):
        solution = solve(GOAL_STATE, GOAL_STATE)

        assert solution == [GOAL_STATE]


class TestSolvesSimplePuzzles:
    def test_solution_is_valid_and_optimal_for_a_one_move_puzzle(self):
        solution = solve(ONE_MOVE_AWAY, GOAL_STATE)

        assert solution is not None
        _assert_valid_solution(solution, ONE_MOVE_AWAY, GOAL_STATE)
        assert len(solution) - 1 == _bfs_optimal_length(ONE_MOVE_AWAY, GOAL_STATE)

    def test_solution_is_valid_and_optimal_for_a_two_move_puzzle(self):
        solution = solve(TWO_MOVES_AWAY, GOAL_STATE)

        assert solution is not None
        _assert_valid_solution(solution, TWO_MOVES_AWAY, GOAL_STATE)
        assert len(solution) - 1 == _bfs_optimal_length(TWO_MOVES_AWAY, GOAL_STATE)

    def test_solution_is_valid_and_optimal_for_a_multi_move_puzzle(self):
        solution = solve(THREE_MOVES_AWAY, GOAL_STATE)

        assert solution is not None
        _assert_valid_solution(solution, THREE_MOVES_AWAY, GOAL_STATE)
        assert len(solution) - 1 == _bfs_optimal_length(THREE_MOVES_AWAY, GOAL_STATE)
