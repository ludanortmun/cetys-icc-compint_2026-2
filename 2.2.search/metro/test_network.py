"""Checklist-style grading tests for the MetroNetwork assignment.

Pytest groups the report by class: Part 1 covers core graph methods, Part 2
covers mutable service state, and Part 3 covers the extra-credit assistant
method. Each test creates its own registry and network, so no configured TUI
topology affects grading.
"""

from __future__ import annotations

from collections.abc import Iterable

import pytest

from metro.network import MetroNetwork, RouteSegment
from metro.station import Station, StationRegistry


def build_network(
    station_ids: Iterable[str],
    lines: dict[str, list[str]],
) -> MetroNetwork:
    """Create an isolated network and populate it with the supplied lines."""
    registry = StationRegistry.from_stations(
        [
            Station(station_id, f"Station {station_id}")
            for station_id in station_ids
        ]
    )
    network = MetroNetwork(registry)
    for line_name, line_station_ids in lines.items():
        network.add_line(line_name, line_station_ids)
    return network


def connected_ids(network: MetroNetwork, station_id: str) -> list[str]:
    return [station.id for station in network.get_connected_stations(station_id)]


def route_ids(
    network: MetroNetwork,
    from_station_id: str,
    to_station_id: str,
    search_type: str = "bfs",
) -> list[str] | None:
    route = network.find_route(
        from_station_id,
        to_station_id,
        search_type,  # type: ignore[arg-type]
    )
    return None if route is None else [station.id for station in route]


class TestPart1AddLine:
    """Part 1: add_line creates and validates graph connections."""

    def test_add_line_connects_consecutive_stations(self) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B", "C"]}
        )

        assert connected_ids(network, "A") == ["B"]
        assert connected_ids(network, "B") == ["A", "C"]
        assert connected_ids(network, "C") == ["B"]

    def test_add_line_keeps_connections_from_multiple_lines(self) -> None:
        network = build_network(
            ["A", "B", "C", "D"],
            {"Red": ["A", "B", "C"], "Blue": ["C", "D"]},
        )

        assert connected_ids(network, "C") == ["B", "D"]

    def test_add_line_rejects_a_duplicate_line_name(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        with pytest.raises(ValueError):
            network.add_line("Red", ["A"])

    def test_add_line_rejects_an_unknown_station(self) -> None:
        network = build_network(["A"], {})

        with pytest.raises(ValueError):
            network.add_line("Red", ["A", "UNKNOWN"])


class TestPart1GetConnectedStations:
    """Part 1: get_connected_stations reads direct graph neighbors."""

    def test_get_connected_stations_returns_station_objects(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        assert network.get_connected_stations("A") == [
            Station("B", "Station B")
        ]

    def test_get_connected_stations_returns_an_empty_list_for_an_isolated_station(
        self,
    ) -> None:
        network = build_network(["A", "B"], {})

        assert network.get_connected_stations("A") == []

    def test_get_connected_stations_rejects_an_unknown_station(self) -> None:
        network = build_network(["A"], {})

        with pytest.raises(ValueError):
            network.get_connected_stations("UNKNOWN")


class TestPart1FindRoute:
    """Part 1: find_route searches the graph with BFS or DFS."""

    def test_find_route_bfs_returns_a_shortest_route(self) -> None:
        network = build_network(
            ["A", "B", "C", "D", "E"],
            {
                "First": ["A", "B", "D", "E"],
                "Shortcut": ["A", "C", "E"],
            },
        )

        assert route_ids(network, "A", "E", "bfs") == ["A", "C", "E"]

    def test_find_route_dfs_follows_depth_first_order(self) -> None:
        network = build_network(
            ["A", "B", "C", "D", "E"],
            {
                "First": ["A", "B", "D", "E"],
                "Shortcut": ["A", "C", "E"],
            },
        )

        assert route_ids(network, "A", "E", "dfs") == ["A", "B", "D", "E"]

    def test_find_route_returns_the_origin_for_a_same_station_trip(self) -> None:
        network = build_network(["A"], {})

        assert route_ids(network, "A", "A") == ["A"]

    def test_find_route_returns_none_when_no_route_exists(self) -> None:
        network = build_network(["A", "B", "C"], {"Red": ["A", "B"]})

        assert network.find_route("A", "C") is None

    @pytest.mark.parametrize(
        ("from_station_id", "to_station_id"),
        [("UNKNOWN", "A"), ("A", "UNKNOWN")],
        ids=["unknown-origin", "unknown-destination"],
    )
    def test_find_route_rejects_an_unknown_station(
        self, from_station_id: str, to_station_id: str
    ) -> None:
        network = build_network(["A"], {})

        with pytest.raises(ValueError):
            network.find_route(from_station_id, to_station_id)

    def test_find_route_rejects_an_unknown_search_type(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        with pytest.raises(ValueError):
            network.find_route("A", "B", "astar")  # type: ignore[arg-type]


class TestPart1AdjacencyList:
    """Part 1: as_adjacency_list exposes every station's open neighbors."""

    def test_as_adjacency_list_includes_connected_and_isolated_stations(
        self,
    ) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B"]}
        )

        assert network.as_adjacency_list() == {
            "A": ["B"],
            "B": ["A"],
            "C": [],
        }


class TestPart1AdjacencyMatrix:
    """Part 1: as_adjacency_matrix follows StationRegistry indexes."""

    def test_as_adjacency_matrix_marks_connections_at_registry_indexes(
        self,
    ) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B"]}
        )

        assert network.as_adjacency_matrix() == [
            [False, True, False],
            [True, False, False],
            [False, False, False],
        ]


class TestPart2CloseSegment:
    """Part 2: close_segment introduces directed unavailable-service state."""

    def test_close_segment_removes_the_forward_connection(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        network.close_segment("A", "B")

        assert connected_ids(network, "A") == []

    def test_close_segment_keeps_the_reverse_connection_open(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        network.close_segment("A", "B")

        assert connected_ids(network, "B") == ["A"]

    def test_close_segment_updates_the_adjacency_list(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        network.close_segment("A", "B")

        assert network.as_adjacency_list()["A"] == []

    def test_close_segment_updates_the_adjacency_matrix(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        network.close_segment("A", "B")

        assert network.as_adjacency_matrix() == [
            [False, False],
            [True, False],
        ]

    def test_close_segment_prevents_routes_using_that_direction(self) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B", "C"]}
        )

        network.close_segment("B", "C")

        assert network.find_route("A", "C") is None

    def test_close_segment_preserves_routes_in_the_reverse_direction(self) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B", "C"]}
        )

        network.close_segment("B", "C")

        assert route_ids(network, "C", "A") == ["C", "B", "A"]

    def test_close_segment_is_reported_by_get_closed_segments(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        network.close_segment("A", "B")

        assert network.get_closed_segments() == [
            (Station("A", "Station A"), Station("B", "Station B"))
        ]

    def test_close_segment_rejects_an_unknown_station(self) -> None:
        network = build_network(["A"], {})

        with pytest.raises(ValueError):
            network.close_segment("A", "UNKNOWN")

    def test_close_segment_rejects_a_nonexistent_connection(self) -> None:
        network = build_network(["A", "B"], {})

        with pytest.raises(ValueError):
            network.close_segment("A", "B")

    def test_close_segment_rejects_an_already_closed_direction(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})
        network.close_segment("A", "B")

        with pytest.raises(ValueError):
            network.close_segment("A", "B")

    def test_close_segment_affects_extra_credit_routes(self) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B", "C"]}
        )
        network.close_segment("B", "C")

        assert network.find_route_with_lines("A", "C") is None


class TestPart2OpenSegment:
    """Part 2: open_segment removes closure state in the chosen direction."""

    def test_open_segment_restores_the_forward_connection(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})
        network.close_segment("A", "B")

        network.open_segment("A", "B")

        assert connected_ids(network, "A") == ["B"]

    def test_open_segment_restores_routes(self) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B", "C"]}
        )
        network.close_segment("B", "C")

        network.open_segment("B", "C")

        assert route_ids(network, "A", "C") == ["A", "B", "C"]

    def test_open_segment_removes_the_closed_segment_record(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})
        network.close_segment("A", "B")

        network.open_segment("A", "B")

        assert network.get_closed_segments() == []

    def test_open_segment_rejects_a_direction_that_is_not_closed(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})

        with pytest.raises(ValueError):
            network.open_segment("A", "B")

    def test_open_segment_rejects_the_reverse_direction_when_only_forward_is_closed(
        self,
    ) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})
        network.close_segment("A", "B")

        with pytest.raises(ValueError):
            network.open_segment("B", "A")


class TestPart2GetClosedSegments:
    """Part 2: get_closed_segments presents closure data as Station objects."""

    def test_get_closed_segments_preserves_each_closure_direction(self) -> None:
        network = build_network(["A", "B"], {"Red": ["A", "B"]})
        network.close_segment("A", "B")
        network.close_segment("B", "A")

        assert set(network.get_closed_segments()) == {
            (Station("A", "Station A"), Station("B", "Station B")),
            (Station("B", "Station B"), Station("A", "Station A")),
        }


class TestPart3FindRouteWithLines:
    """Part 3 extra credit: find_route_with_lines adds metro business logic."""

    def test_find_route_with_lines_groups_consecutive_segments_on_one_line(
        self,
    ) -> None:
        network = build_network(
            ["A", "B", "C"], {"Red": ["A", "B", "C"]}
        )

        assert network.find_route_with_lines("A", "C") == [
            RouteSegment("Red", "A", "C")
        ]

    def test_find_route_with_lines_creates_a_segment_for_each_line_change(
        self,
    ) -> None:
        network = build_network(
            ["A", "B", "C", "D"],
            {"Red": ["A", "B", "C"], "Blue": ["C", "D"]},
        )

        assert network.find_route_with_lines("A", "D") == [
            RouteSegment("Red", "A", "C"),
            RouteSegment("Blue", "C", "D"),
        ]

    def test_find_route_with_lines_returns_none_when_no_route_exists(self) -> None:
        network = build_network(
            ["A", "B", "C", "D"],
            {"Red": ["A", "B"], "Blue": ["C", "D"]},
        )

        assert network.find_route_with_lines("A", "D") is None

    def test_find_route_with_lines_returns_no_segments_for_same_station(self) -> None:
        network = build_network(["A"], {})

        assert network.find_route_with_lines("A", "A") == []

    def test_find_route_with_lines_rejects_an_unknown_station(self) -> None:
        network = build_network(["A"], {})

        with pytest.raises(ValueError):
            network.find_route_with_lines("A", "UNKNOWN")
