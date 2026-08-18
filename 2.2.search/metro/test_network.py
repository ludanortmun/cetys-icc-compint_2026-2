"""Topology-independent pytest contract tests for ``MetroNetwork`` submissions.

Each test creates a fresh ``StationRegistry`` and passes it to ``MetroNetwork``.
This prevents the configured application topology from affecting grades.
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
    station_registry = StationRegistry.from_stations(
        [
            Station(station_id, f"Station {station_id}")
            for station_id in station_ids
        ]
    )
    network = MetroNetwork(station_registry)
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


def test_add_line_builds_undirected_connections() -> None:
    network = build_network(
        ["A", "B", "C", "D"],
        {"Red": ["A", "B", "C"], "Blue": ["C", "D"]},
    )

    assert connected_ids(network, "A") == ["B"]
    assert connected_ids(network, "B") == ["A", "C"]
    assert connected_ids(network, "C") == ["B", "D"]
    assert connected_ids(network, "D") == ["C"]


def test_add_line_rejects_duplicate_names_and_unknown_stations() -> None:
    network = build_network(["A", "B"], {})
    network.add_line("Red", ["A", "B"])

    with pytest.raises(ValueError):
        network.add_line("Red", ["A"])
    with pytest.raises(ValueError):
        network.add_line("Blue", ["A", "UNKNOWN"])


def test_connected_stations_returns_station_objects_and_validates_id() -> None:
    network = build_network(["A", "B", "C"], {"Red": ["A", "B"]})

    connected = network.get_connected_stations("A")

    assert connected == [Station("B", "Station B")]
    assert all(isinstance(station, Station) for station in connected)
    assert network.get_connected_stations("C") == []
    with pytest.raises(ValueError):
        network.get_connected_stations("UNKNOWN")


def test_bfs_returns_shortest_route_and_dfs_follows_depth_first_order() -> None:
    network = build_network(
        ["A", "B", "C", "D", "E"],
        {
            "First": ["A", "B", "D", "E"],
            "Shortcut": ["A", "C", "E"],
        },
    )

    assert route_ids(network, "A", "E", "bfs") == ["A", "C", "E"]
    assert route_ids(network, "A", "E", "dfs") == ["A", "B", "D", "E"]


def test_route_handles_same_station_no_route_and_invalid_inputs() -> None:
    network = build_network(["A", "B", "C"], {"Red": ["A", "B"]})

    assert route_ids(network, "A", "A") == ["A"]
    assert network.find_route("A", "C") is None
    with pytest.raises(ValueError):
        network.find_route("UNKNOWN", "A")
    with pytest.raises(ValueError):
        network.find_route("A", "UNKNOWN")
    with pytest.raises(ValueError):
        network.find_route("A", "B", "astar")  # type: ignore[arg-type]


def test_adjacency_views_include_all_stations_and_registry_indexes() -> None:
    network = build_network(
        ["A", "B", "C", "D"],
        {"Red": ["A", "B", "C"]},
    )

    assert network.as_adjacency_list() == {
        "A": ["B"],
        "B": ["A", "C"],
        "C": ["B"],
        "D": [],
    }
    assert network.as_adjacency_matrix() == [
        [False, True, False, False],
        [True, False, True, False],
        [False, True, False, False],
        [False, False, False, False],
    ]


def test_closing_segment_only_blocks_its_configured_direction() -> None:
    network = build_network(
        ["A", "B", "C", "D"],
        {"Red": ["A", "B", "C"], "Blue": ["B", "D"]},
    )

    network.close_segment("B", "C")

    assert connected_ids(network, "B") == ["A", "D"]
    assert connected_ids(network, "C") == ["B"]
    assert "C" not in network.as_adjacency_list()["B"]
    assert network.as_adjacency_matrix()[1][2] is False
    assert network.as_adjacency_matrix()[2][1] is True
    assert network.find_route("A", "C") is None
    assert route_ids(network, "C", "A") == ["C", "B", "A"]
    assert {
        (start.id, end.id)
        for start, end in network.get_closed_segments()
    } == {("B", "C")}

    network.open_segment("B", "C")

    assert connected_ids(network, "B") == ["A", "C", "D"]
    assert route_ids(network, "A", "C") == ["A", "B", "C"]
    assert network.get_closed_segments() == []


def test_segment_operations_validate_existing_and_closed_state() -> None:
    network = build_network(["A", "B", "C"], {"Red": ["A", "B"]})

    with pytest.raises(ValueError):
        network.close_segment("A", "C")
    with pytest.raises(ValueError):
        network.close_segment("A", "UNKNOWN")
    with pytest.raises(ValueError):
        network.open_segment("A", "B")

    network.close_segment("A", "B")
    with pytest.raises(ValueError):
        network.close_segment("A", "B")

    network.close_segment("B", "A")


def test_route_with_lines_groups_contiguous_segments_and_transfers() -> None:
    network = build_network(
        ["A", "B", "C", "D", "E"],
        {"Red": ["A", "B", "C"], "Blue": ["C", "D", "E"]},
    )

    assert network.find_route_with_lines("A", "E") == [
        RouteSegment("Red", "A", "C"),
        RouteSegment("Blue", "C", "E"),
    ]


def test_route_with_lines_respects_closures_and_validates_routes() -> None:
    network = build_network(
        ["A", "B", "C", "D"],
        {"Red": ["A", "B"], "Blue": ["C", "D"]},
    )

    assert network.find_route_with_lines("A", "D") is None
    assert network.find_route_with_lines("A", "A") == []
    with pytest.raises(ValueError):
        network.find_route_with_lines("A", "UNKNOWN")

    network = build_network(
        ["A", "B", "C"], {"Red": ["A", "B", "C"]}
    )
    network.close_segment("B", "C")
    assert network.find_route_with_lines("A", "C") is None
