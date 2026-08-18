"""Test-only reference network and sample topology.

This module is deliberately independent from the student-owned topology data.
Use ``build_sample_network()`` when a working MetroNetwork-compatible object is
needed while developing or manually trying the TUI.  It is not imported by
production modules.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from typing import Literal

from metro.network import MetroNetwork, RouteSegment
from metro.station import Station, StationRegistry


SAMPLE_STATIONS = [
    Station("HBR", "Harbor"),
    Station("MKT", "Market"),
    Station("MSM", "Museum"),
    Station("PRK", "Park"),
    Station("UNI", "University"),
    Station("AIR", "Airport"),
]
"""A small network with a transfer and a loop for development use."""

SAMPLE_STATION_REGISTRY = StationRegistry.from_stations(SAMPLE_STATIONS)
SAMPLE_LINE_REGISTRY: dict[str, list[str]] = {
    "Red": ["HBR", "MKT", "MSM", "PRK"],
    "Blue": ["UNI", "MKT", "AIR"],
    "Green": ["MSM", "AIR"],
}


class ReferenceMetroNetwork(MetroNetwork):
    """A complete, deterministic implementation used only for test/dev work."""

    def __init__(self, station_registry: StationRegistry | None = None):
        self._station_registry = (
            SAMPLE_STATION_REGISTRY
            if station_registry is None
            else station_registry
        )
        self._stations = {
            station.id: station
            for station in self._station_registry.all_stations()
        }
        self._station_ids = tuple(self._stations)
        self._station_positions = {
            station_id: index for index, station_id in enumerate(self._station_ids)
        }
        self._adjacency = {station_id: [] for station_id in self._station_ids}
        self._line_names: set[str] = set()
        self._edge_lines: dict[frozenset[str], list[str]] = {}
        self._closed_segments: set[frozenset[str]] = set()

    def add_line(self, name: str, station_ids: list[str]):
        if name in self._line_names:
            raise ValueError(f"Line already exists: {name}")
        for station_id in station_ids:
            self._require_station(station_id)

        self._line_names.add(name)
        for from_station_id, to_station_id in zip(station_ids, station_ids[1:]):
            edge = frozenset((from_station_id, to_station_id))
            lines = self._edge_lines.setdefault(edge, [])
            lines.append(name)
            if to_station_id not in self._adjacency[from_station_id]:
                self._adjacency[from_station_id].append(to_station_id)
            if from_station_id not in self._adjacency[to_station_id]:
                self._adjacency[to_station_id].append(from_station_id)

    def get_connected_stations(self, station_id: str) -> list[Station]:
        self._require_station(station_id)
        return [
            self._stations[neighbor_id]
            for neighbor_id in self._adjacency[station_id]
            if self._edge(station_id, neighbor_id) not in self._closed_segments
        ]

    def find_route(
        self,
        from_station_id: str,
        to_station_id: str,
        search_type: Literal["bfs", "dfs"] = "bfs",
    ) -> list[Station] | None:
        self._require_station(from_station_id)
        self._require_station(to_station_id)
        self._require_search_type(search_type)

        if from_station_id == to_station_id:
            return [self._stations[from_station_id]]

        previous = self._search(from_station_id, to_station_id, search_type)
        if to_station_id not in previous:
            return None
        return [
            self._stations[station_id]
            for station_id in self._path_from_previous(
                previous, from_station_id, to_station_id
            )
        ]

    def as_adjacency_list(self) -> dict[str, list[str]]:
        return {
            station_id: [
                station.id for station in self.get_connected_stations(station_id)
            ]
            for station_id in self._station_ids
        }

    def as_adjacency_matrix(self) -> list[list[bool]]:
        matrix = [
            [False for _ in self._station_ids] for _ in self._station_ids
        ]
        for station_id, neighbors in self.as_adjacency_list().items():
            from_index = self._station_positions[station_id]
            for neighbor_id in neighbors:
                matrix[from_index][self._station_positions[neighbor_id]] = True
        return matrix

    def close_segment(self, from_station_id: str, to_station_id: str):
        edge = self._validated_edge(from_station_id, to_station_id)
        if edge in self._closed_segments:
            raise ValueError("Segment is already closed")
        self._closed_segments.add(edge)

    def open_segment(self, from_station_id: str, to_station_id: str):
        edge = self._validated_edge(from_station_id, to_station_id)
        if edge not in self._closed_segments:
            raise ValueError("Segment is not closed")
        self._closed_segments.remove(edge)

    def get_closed_segments(self) -> list[tuple[Station, Station]]:
        return [
            (self._stations[from_station_id], self._stations[to_station_id])
            for from_station_id, to_station_id in sorted(
                (self._ordered_edge(edge) for edge in self._closed_segments),
                key=lambda segment: (
                    self._station_positions[segment[0]],
                    self._station_positions[segment[1]],
                ),
            )
        ]

    def find_route_with_lines(
        self,
        from_station_id: str,
        to_station_id: str,
        search_type: Literal["bfs", "dfs"] = "bfs",
    ) -> list[RouteSegment] | None:
        route = self.find_route(from_station_id, to_station_id, search_type)
        if route is None:
            return None

        segments: list[RouteSegment] = []
        for from_station, to_station in zip(route, route[1:]):
            line = self._edge_lines[self._edge(from_station.id, to_station.id)][0]
            if segments and segments[-1].line == line:
                segments[-1].exit_station_id = to_station.id
            else:
                segments.append(RouteSegment(line, from_station.id, to_station.id))
        return segments

    def _search(
        self,
        from_station_id: str,
        to_station_id: str,
        search_type: Literal["bfs", "dfs"],
    ) -> dict[str, str | None]:
        previous: dict[str, str | None] = {from_station_id: None}

        if search_type == "bfs":
            pending: deque[str] = deque((from_station_id,))
            while pending:
                current_station_id = pending.popleft()
                for neighbor in self.get_connected_stations(current_station_id):
                    if neighbor.id in previous:
                        continue
                    previous[neighbor.id] = current_station_id
                    if neighbor.id == to_station_id:
                        return previous
                    pending.append(neighbor.id)
            return previous

        pending = [
            (from_station_id, iter(self.get_connected_stations(from_station_id)))
        ]
        while pending:
            current_station_id, neighbors = pending[-1]
            try:
                neighbor = next(neighbors)
            except StopIteration:
                pending.pop()
                continue
            if neighbor.id in previous:
                continue
            previous[neighbor.id] = current_station_id
            if neighbor.id == to_station_id:
                return previous
            pending.append(
                (neighbor.id, iter(self.get_connected_stations(neighbor.id)))
            )
        return previous

    @staticmethod
    def _path_from_previous(
        previous: Mapping[str, str | None],
        from_station_id: str,
        to_station_id: str,
    ) -> list[str]:
        path = [to_station_id]
        while path[-1] != from_station_id:
            parent = previous[path[-1]]
            if parent is None:
                break
            path.append(parent)
        path.reverse()
        return path

    def _validated_edge(
        self, from_station_id: str, to_station_id: str
    ) -> frozenset[str]:
        self._require_station(from_station_id)
        self._require_station(to_station_id)
        edge = self._edge(from_station_id, to_station_id)
        if edge not in self._edge_lines:
            raise ValueError("Segment does not exist")
        return edge

    def _ordered_edge(self, edge: frozenset[str]) -> tuple[str, str]:
        ordered_ids = sorted(edge, key=self._station_positions.__getitem__)
        if len(ordered_ids) == 1:
            return ordered_ids[0], ordered_ids[0]
        return ordered_ids[0], ordered_ids[1]

    @staticmethod
    def _edge(from_station_id: str, to_station_id: str) -> frozenset[str]:
        return frozenset((from_station_id, to_station_id))

    def _require_station(self, station_id: str):
        if station_id not in self._stations:
            raise ValueError(f"Unknown station ID: {station_id}")

    @staticmethod
    def _require_search_type(search_type: Literal["bfs", "dfs"]):
        if search_type not in {"bfs", "dfs"}:
            raise ValueError(f"Unsupported search type: {search_type}")


def build_sample_network() -> ReferenceMetroNetwork:
    """Return the complete made-up topology for dev and manual TUI exercises."""
    network = ReferenceMetroNetwork()
    for line_name, station_ids in SAMPLE_LINE_REGISTRY.items():
        network.add_line(line_name, station_ids)
    return network
