# 4.2 Eight-puzzle

## Introduction

The 8-puzzle is a 3x3 sliding tile puzzle: eight numbered tiles and one
blank space, arranged in a grid. A move slides a tile adjacent to the blank
into the blank's position; the goal is to reach a target arrangement using
as few moves as possible.

Each arrangement of the puzzle is a **state**, and each move connects two
states. This is a graph, just like the ones in earlier activities, except
its ~180,000 reachable states are never built up front: instead, the
neighbors of a state are computed on demand, only for the states an
algorithm actually needs to look at.

In this activity you will implement that neighbor generation, and then use
it to build an A* solver for the puzzle.

## Setup

From this project directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run and validate

Run the TUI with:

```bash
python -m puzzle.main
```

Run the grading tests with:

```bash
pytest
```

Run the tests for a single part with:

```bash
pytest puzzle/test_state.py        # Part 1: Puzzle.get_neighboring_states
pytest puzzle/test_heuristics.py   # Part 2: manhattan_distance_heuristic
pytest puzzle/test_solver.py       # Part 2: PuzzleSolver.solve
```

## Student instructions

Your implementation belongs in `puzzle/state.py`, `puzzle/heuristics.py`,
and `puzzle/solver.py`. Do not change the public method signatures there.

### Part 1: Representing states as a graph

Implement `Puzzle.get_neighboring_states` in `puzzle/state.py`. A board is
represented as a tuple of tuples, with `0` marking the blank tile. Given a
`Puzzle`, this method must return every state reachable by sliding a single
tile into the blank space (i.e. moving the blank up, down, left, or right,
whenever that keeps the blank on the board).

The "Play a puzzle manually" option in the TUI lets you interactively step
through the states this method produces, which is useful for checking your
implementation by hand. This TUI option is only for your convenience and is
not part of the grading tests; the `pytest` test suite is the only source
of truth for grading.

### Part 2: Solving with A*

Implement `manhattan_distance_heuristic` in `puzzle/heuristics.py`: the sum,
over every non-blank tile, of the Manhattan distance between that tile's
current position and its position in the goal state.

Then implement `PuzzleSolver.solve` in `puzzle/solver.py`. It must run A*
from a start state to a goal state, treating every move as having a cost
of 1, using `get_neighboring_states` to expand a state only when the search
needs it, and `self.heuristic` to prioritize which state to expand next. It
must return the sequence of states from start to goal (both included). You
may assume the goal is always reachable from the start.

The "Watch A* solve a puzzle" option in the TUI plays back the resulting
solution one move at a time. This TUI option is only for your convenience
and is not part of the grading tests; the `pytest` test suite is the only
source of truth for grading.
