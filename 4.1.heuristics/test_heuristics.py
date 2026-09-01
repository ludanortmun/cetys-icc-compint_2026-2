import math

import pytest

from heuristics import chebyshev_distance, euclidean_distance, manhattan_distance


class TestManhattanDistance:
    @pytest.mark.parametrize(
        "node, target, expected",
        [
            ((2, 3), (5, 7), 7),
            ((0, 0), (0, 0), 0),
            ((0, 0), (3, 4), 7),
            ((3, 4), (0, 0), 7),
            ((-2, -2), (2, 2), 8),
        ],
        ids=[
            "lecture-example",
            "same-point",
            "forward",
            "symmetric",
            "negative-coordinates",
        ],
    )
    def test_known_values(self, node, target, expected):
        assert manhattan_distance(node, target) == expected


class TestEuclideanDistance:
    @pytest.mark.parametrize(
        "node, target, expected",
        [
            ((2, 3), (5, 7), 5.0),
            ((0, 0), (0, 0), 0.0),
            ((0, 0), (3, 4), 5.0),
            ((3, 4), (0, 0), 5.0),
            ((0, 0), (1, 1), math.sqrt(2)),
        ],
        ids=[
            "lecture-example",
            "same-point",
            "forward",
            "symmetric",
            "unit-diagonal",
        ],
    )
    def test_known_values(self, node, target, expected):
        assert euclidean_distance(node, target) == pytest.approx(expected)


class TestChebyshevDistance:
    @pytest.mark.parametrize(
        "node, target, expected",
        [
            ((2, 3), (5, 7), 4),
            ((0, 0), (0, 0), 0),
            ((0, 0), (3, 4), 4),
            ((3, 4), (0, 0), 4),
            ((0, 0), (5, 1), 5),
        ],
        ids=[
            "lecture-example",
            "same-point",
            "forward",
            "symmetric",
            "dominant-axis",
        ],
    )
    def test_known_values(self, node, target, expected):
        assert chebyshev_distance(node, target) == expected


class TestHeuristicOrdering:
    def test_chebyshev_never_exceeds_euclidean_which_never_exceeds_manhattan(self):
        # For any pair of points, chebyshev <= euclidean <= manhattan.
        node, target = (1, 8), (6, 2)

        assert chebyshev_distance(
            node, target) <= euclidean_distance(node, target)
        assert euclidean_distance(
            node, target) <= manhattan_distance(node, target)
