"""
Unit tests for adjacency_matrix.py

These tests validate that your hardcoded adjacency matrices correctly
represent the graphs described in the docstrings, and that edge_exists()
and get_neighbors() work correctly.

The expected representations are not included in this file; they are
loaded from fixtures/expected_graphs.joblib via the `expected` fixture
defined in conftest.py.

Run with: pytest test_adjacency_matrix.py
"""
import itertools

import pytest

from adjacency_matrix import (
    linear_graph_adjacency_matrix,
    branching_graph_adjacency_matrix,
    cycle_graph_adjacency_matrix,
    edge_exists,
    get_neighbors,
)

# Node counts for each graph, as shown in the docstrings/diagrams. Used to
# exhaustively parametrize the edge_exists/get_neighbors tests below.
GRAPH_SIZES = {
    "linear": 3,
    "branching": 5,
    "cycle": 4,
}

ALL_NODE_PAIRS = [
    (graph, i, j)
    for graph, size in GRAPH_SIZES.items()
    for i, j in itertools.product(range(size), range(size))
]
ALL_NODE_PAIR_IDS = [f"{graph}-node{i}-node{j}" for graph, i, j in ALL_NODE_PAIRS]

ALL_NODES = [
    (graph, node) for graph, size in GRAPH_SIZES.items() for node in range(size)
]
ALL_NODE_IDS = [f"{graph}-node{node}" for graph, node in ALL_NODES]


def assert_matches_expected_matrix(actual, expected_matrix):
    # Dimensions must match: same number of rows, and each row the same length.
    assert len(actual) == len(expected_matrix), "Matrix has the wrong number of rows"
    for i, (actual_row, expected_row) in enumerate(zip(actual, expected_matrix)):
        assert len(actual_row) == len(expected_row), f"Row {i} has the wrong length"

    assert actual == expected_matrix


# ---------------------------------------------------------------------------
# linear_graph_adjacency_matrix
#
#   0 ─── 1 ─── 2
# ---------------------------------------------------------------------------
class TestLinearGraphAdjacencyMatrix:
    def test_matches_expected(self, expected):
        assert_matches_expected_matrix(
            linear_graph_adjacency_matrix(), expected["linear_matrix"]
        )


# ---------------------------------------------------------------------------
# branching_graph_adjacency_matrix
#
#         1
#         │
#   0 ─── 2 ─── 3
#         │
#         4
# ---------------------------------------------------------------------------
class TestBranchingGraphAdjacencyMatrix:
    def test_matches_expected(self, expected):
        assert_matches_expected_matrix(
            branching_graph_adjacency_matrix(), expected["branching_matrix"]
        )


# ---------------------------------------------------------------------------
# cycle_graph_adjacency_matrix
#
#   0 ─── 1
#   │     │
#   3 ─── 2
# ---------------------------------------------------------------------------
class TestCycleGraphAdjacencyMatrix:
    def test_matches_expected(self, expected):
        assert_matches_expected_matrix(
            cycle_graph_adjacency_matrix(), expected["cycle_matrix"]
        )


# ---------------------------------------------------------------------------
# edge_exists
#
# Exercised directly against the known-good expected matrices, independent
# of whatever the student's own graph-builder functions return. Every
# (from_node, to_node) combination is checked, for all 3 known graphs.
# ---------------------------------------------------------------------------
class TestEdgeExists:
    @pytest.mark.parametrize("graph, i, j", ALL_NODE_PAIRS, ids=ALL_NODE_PAIR_IDS)
    def test_all_node_pairs(self, expected, graph, i, j):
        matrix = expected[f"{graph}_matrix"]
        assert edge_exists(matrix, i, j) is matrix[i][j]

    @pytest.mark.parametrize("graph", GRAPH_SIZES, ids=GRAPH_SIZES)
    def test_undirected_symmetry(self, expected, graph):
        matrix = expected[f"{graph}_matrix"]
        size = GRAPH_SIZES[graph]
        for i, j in itertools.product(range(size), range(size)):
            assert edge_exists(matrix, i, j) == edge_exists(matrix, j, i), (
                f"edge_exists({graph}, {i}, {j}) should equal "
                f"edge_exists({graph}, {j}, {i})"
            )


# ---------------------------------------------------------------------------
# get_neighbors
#
# Exercised directly against the known-good expected matrices, independent
# of whatever the student's own graph-builder functions return. Every node
# is checked, for all 3 known graphs.
# ---------------------------------------------------------------------------
class TestGetNeighbors:
    @pytest.mark.parametrize("graph, node", ALL_NODES, ids=ALL_NODE_IDS)
    def test_all_nodes(self, expected, graph, node):
        matrix = expected[f"{graph}_matrix"]
        expected_neighbors = [
            neighbor for neighbor, is_connected in enumerate(matrix[node]) if is_connected
        ]
        assert sorted(get_neighbors(matrix, node)) == expected_neighbors
