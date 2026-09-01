# 4.1 Heuristics

## Introduction

Search algorithms such as Dijkstra find the lowest-cost path by expanding
nodes in order of their accumulated cost, without regard for where the
target is. A **heuristic** `h(n)` estimates the remaining cost from a node
`n` to the target, which lets an informed search algorithm (such as A*)
prioritize the most promising nodes first.

Not every heuristic is a good fit for every problem: the right choice
depends on which directions an agent can move in and how much each kind of
move costs. Using a heuristic that overestimates the true remaining cost
can cause a search algorithm to miss the optimal path.

In this activity you will implement three common distance heuristics used
on grids: Manhattan, Euclidean, and Chebyshev.

## Setup

From this directory, create and activate a virtual environment, then
install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

With the virtual environment activated:

```bash
pytest
```

Use `pytest -v` for verbose output showing each individual test case.

## Student instructions

Implement, in `heuristics.py`:

- `manhattan_distance`
- `euclidean_distance`
- `chebyshev_distance`

Each function takes a `node` and a `target`, both `(x, y)` tuples, and
returns the estimated remaining cost between them, as described in each
function's docstring.

As you implement each one, think about which grid movement model it fits:
how many directions an agent can move in, and how much a diagonal step
costs relative to an orthogonal one. That is the same judgment call you
will need to make later when picking a heuristic for A*.
