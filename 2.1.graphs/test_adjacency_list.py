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

Run with: pytest test_adjacency_list.py
"""
import itertools

import pytest

from adjacency_list import (
    linear_graph_adjacency_list,
    branching_graph_adjacency_list,
    cycle_graph_adjacency_list,
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
# Every (from_node, to_node) combination is checked, for all 3 known graphs.
# ---------------------------------------------------------------------------
class TestEdgeExists:
    @pytest.mark.parametrize("graph, i, j", ALL_NODE_PAIRS, ids=ALL_NODE_PAIR_IDS)
    def test_all_node_pairs(self, expected, graph, i, j):
        adjacency_list = expected[f"{graph}_list"]
        assert edge_exists(adjacency_list, i, j) is (j in adjacency_list[i])

    @pytest.mark.parametrize("graph", GRAPH_SIZES, ids=GRAPH_SIZES)
    def test_undirected_symmetry(self, expected, graph):
        adjacency_list = expected[f"{graph}_list"]
        size = GRAPH_SIZES[graph]
        for i, j in itertools.product(range(size), range(size)):
            assert edge_exists(adjacency_list, i, j) == edge_exists(adjacency_list, j, i), (
                f"edge_exists({graph}, {i}, {j}) should equal "
                f"edge_exists({graph}, {j}, {i})"
            )


# ---------------------------------------------------------------------------
# get_neighbors
#
# Exercised directly against the known-good expected adjacency lists,
# independent of whatever the student's own graph-builder functions return.
# Every node is checked, for all 3 known graphs.
# ---------------------------------------------------------------------------
class TestGetNeighbors:
    @pytest.mark.parametrize("graph, node", ALL_NODES, ids=ALL_NODE_IDS)
    def test_all_nodes(self, expected, graph, node):
        adjacency_list = expected[f"{graph}_list"]
        expected_neighbors = set(adjacency_list[node])
        assert set(get_neighbors(adjacency_list, node)) == expected_neighbors
