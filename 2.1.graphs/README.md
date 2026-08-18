# 2.1 Graphs

In this activity you will implement two common ways of representing a graph
in code:

- **Adjacency matrix** (`adjacency_matrix.py`): a 2D grid of booleans where
  `matrix[i][j]` is `True` if there is an edge between node `i` and node `j`.
- **Adjacency list** (`adjacency_list.py`): a list where entry `i` contains
  the list of neighbors of node `i`.

For both representations you must hardcode the graph shown in each
function's docstring, and implement `edge_exists` and `get_neighbors`.

## Setup

From this directory, create and activate a virtual environment, then install
the dependencies:

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

Or run the tests for a single file:

```bash
pytest test_adjacency_matrix.py
pytest test_adjacency_list.py
```

Use `pytest -v` for verbose output showing each individual test case
(useful as a checklist while you work through the implementation).

Tests will fail until you've implemented all the functions correctly. Use
the failures as a guide: they tell you which graph, which node pair, or
which method still needs work.
