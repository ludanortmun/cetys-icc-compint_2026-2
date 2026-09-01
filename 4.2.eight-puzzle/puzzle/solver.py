"""
Part 2: A* search over Puzzle states.

PuzzleSolver never builds the state graph up front: it only calls
Puzzle.get_neighboring_states() on the states it actually decides to
expand, generating the graph lazily as the search progresses, and uses a
heuristic to decide which state to expand next.
"""
from collections.abc import Callable
from dataclasses import dataclass, field

from puzzle.heuristics import manhattan_distance_heuristic
from puzzle.state import Puzzle

HeuristicFn = Callable[[Puzzle, Puzzle], float]


@dataclass
class PuzzleSolver:
    heuristic: HeuristicFn = field(default=manhattan_distance_heuristic)

    def solve(self, start: Puzzle, goal: Puzzle) -> list[Puzzle] | None:
        """
        Runs A* from start to goal. Every move has a cost of 1, and
        self.heuristic estimates the remaining cost from a state to goal.
        You may assume goal is always reachable from start.

        Returns the sequence of Puzzle states from start to goal, both
        inclusive, representing an optimal (fewest-moves) solution.
        """
        raise NotImplementedError()
