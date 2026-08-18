"""
Unit tests for adjacency_matrix.py

These tests validate that your hardcoded adjacency matrices correctly
represent the graphs described in the docstrings, and that edge_exists()
and get_neighbors() work correctly.

The expected representations are not included in this file; they are
loaded from fixtures/expected_graphs.joblib via the `expected` fixture
defined in conftest.py.

Run with: uvx pytest test_adjacency_matrix.py
"""
from adjacency_matrix import (
    linear_graph_adjacency_matrix,
    branching_graph_adjacency_matrix,
    cycle_graph_adjacency_matrix,
    edge_exists,
    get_neighbors,
)


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
# of whatever the student's own graph-builder functions return.
# ---------------------------------------------------------------------------
class TestEdgeExists:
    def test_true_for_existing_edge(self, expected):
        matrix = expected["linear_matrix"]
        assert edge_exists(matrix, 0, 1) is True

    def test_false_for_missing_edge(self, expected):
        matrix = expected["linear_matrix"]
        assert edge_exists(matrix, 0, 2) is False

    def test_undirected_symmetry(self, expected):
        matrix = expected["branching_matrix"]
        assert edge_exists(matrix, 0, 2) == edge_exists(matrix, 2, 0)

    def test_across_all_graphs(self, expected):
        cycle = expected["cycle_matrix"]
        assert edge_exists(cycle, 3, 0) is True
        assert edge_exists(cycle, 1, 3) is False


# ---------------------------------------------------------------------------
# get_neighbors
#
# Exercised directly against the known-good expected matrices, independent
# of whatever the student's own graph-builder functions return.
# ---------------------------------------------------------------------------
class TestGetNeighbors:
    def test_linear_endpoints(self, expected):
        matrix = expected["linear_matrix"]
        assert sorted(get_neighbors(matrix, 0)) == [1]
        assert sorted(get_neighbors(matrix, 2)) == [1]

    def test_linear_middle_node(self, expected):
        matrix = expected["linear_matrix"]
        assert sorted(get_neighbors(matrix, 1)) == [0, 2]

    def test_branching_hub_node(self, expected):
        matrix = expected["branching_matrix"]
        assert sorted(get_neighbors(matrix, 2)) == [0, 1, 3, 4]

    def test_branching_leaf_nodes(self, expected):
        matrix = expected["branching_matrix"]
        assert sorted(get_neighbors(matrix, 0)) == [2]
        assert sorted(get_neighbors(matrix, 1)) == [2]
        assert sorted(get_neighbors(matrix, 3)) == [2]
        assert sorted(get_neighbors(matrix, 4)) == [2]

    def test_cycle_every_node_has_two_neighbors(self, expected):
        matrix = expected["cycle_matrix"]
        for node in range(4):
            assert len(get_neighbors(matrix, node)) == 2

    def test_cycle_specific_neighbors(self, expected):
        matrix = expected["cycle_matrix"]
        assert sorted(get_neighbors(matrix, 0)) == [1, 3]
