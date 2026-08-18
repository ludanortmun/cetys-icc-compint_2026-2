"""
Unit tests for adjacency_list.py

These tests validate that your hardcoded adjacency lists correctly
represent the graphs described in the docstrings, and that edge_exists()
and get_neighbors() work correctly.

The expected representations are not included in this file; they are
loaded from fixtures/expected_graphs.joblib via the `expected` fixture
defined in conftest.py. Since neighbor ordering is not significant for an
adjacency list, each node's neighbors are compared as sets rather than
ordered lists; the overall dimensions (number of nodes) are still checked.

Run with: uvx pytest test_adjacency_list.py
"""
from adjacency_list import (
    linear_graph_adjacency_list,
    branching_graph_adjacency_list,
    cycle_graph_adjacency_list,
    edge_exists,
    get_neighbors,
)


def assert_matches_expected_list(actual, expected_list):
    # Dimensions must match: one entry per node.
    assert len(actual) == len(expected_list), "Adjacency list has the wrong number of nodes"

    for node, (actual_neighbors, expected_neighbors) in enumerate(zip(actual, expected_list)):
        assert set(actual_neighbors) == set(expected_neighbors), (
            f"Neighbors of node {node} do not match the expected set"
        )


# ---------------------------------------------------------------------------
# linear_graph_adjacency_list
#
#   0 ─── 1 ─── 2
# ---------------------------------------------------------------------------
class TestLinearGraphAdjacencyList:
    def test_matches_expected(self, expected):
        assert_matches_expected_list(
            linear_graph_adjacency_list(), expected["linear_list"]
        )


# ---------------------------------------------------------------------------
# branching_graph_adjacency_list
#
#         1
#         │
#   0 ─── 2 ─── 3
#         │
#         4
# ---------------------------------------------------------------------------
class TestBranchingGraphAdjacencyList:
    def test_matches_expected(self, expected):
        assert_matches_expected_list(
            branching_graph_adjacency_list(), expected["branching_list"]
        )


# ---------------------------------------------------------------------------
# cycle_graph_adjacency_list
#
#   0 ─── 1
#   │     │
#   3 ─── 2
# ---------------------------------------------------------------------------
class TestCycleGraphAdjacencyList:
    def test_matches_expected(self, expected):
        assert_matches_expected_list(
            cycle_graph_adjacency_list(), expected["cycle_list"]
        )


# ---------------------------------------------------------------------------
# edge_exists
#
# Exercised directly against the known-good expected adjacency lists,
# independent of whatever the student's own graph-builder functions return.
# ---------------------------------------------------------------------------
class TestEdgeExists:
    def test_true_for_existing_edge(self, expected):
        adjacency_list = expected["linear_list"]
        assert edge_exists(adjacency_list, 0, 1) is True

    def test_false_for_missing_edge(self, expected):
        adjacency_list = expected["linear_list"]
        assert edge_exists(adjacency_list, 0, 2) is False

    def test_undirected_symmetry(self, expected):
        adjacency_list = expected["branching_list"]
        assert edge_exists(adjacency_list, 0, 2) == edge_exists(adjacency_list, 2, 0)

    def test_across_all_graphs(self, expected):
        cycle = expected["cycle_list"]
        assert edge_exists(cycle, 3, 0) is True
        assert edge_exists(cycle, 1, 3) is False


# ---------------------------------------------------------------------------
# get_neighbors
#
# Exercised directly against the known-good expected adjacency lists,
# independent of whatever the student's own graph-builder functions return.
# ---------------------------------------------------------------------------
class TestGetNeighbors:
    def test_linear_endpoints(self, expected):
        adjacency_list = expected["linear_list"]
        assert set(get_neighbors(adjacency_list, 0)) == {1}
        assert set(get_neighbors(adjacency_list, 2)) == {1}

    def test_linear_middle_node(self, expected):
        adjacency_list = expected["linear_list"]
        assert set(get_neighbors(adjacency_list, 1)) == {0, 2}

    def test_branching_hub_node(self, expected):
        adjacency_list = expected["branching_list"]
        assert set(get_neighbors(adjacency_list, 2)) == {0, 1, 3, 4}

    def test_branching_leaf_nodes(self, expected):
        adjacency_list = expected["branching_list"]
        assert set(get_neighbors(adjacency_list, 0)) == {2}
        assert set(get_neighbors(adjacency_list, 1)) == {2}
        assert set(get_neighbors(adjacency_list, 3)) == {2}
        assert set(get_neighbors(adjacency_list, 4)) == {2}

    def test_cycle_every_node_has_two_neighbors(self, expected):
        adjacency_list = expected["cycle_list"]
        for node in range(4):
            assert len(get_neighbors(adjacency_list, node)) == 2

    def test_cycle_specific_neighbors(self, expected):
        adjacency_list = expected["cycle_list"]
        assert set(get_neighbors(adjacency_list, 0)) == {1, 3}
