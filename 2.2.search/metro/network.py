from dataclasses import dataclass
from typing import Literal

from metro.station import Station, StationRegistry


@dataclass()
class RouteSegment:
    line: str
    boarding_station_id: str
    exit_station_id: str


class MetroNetwork:
    def __init__(self, station_registry: StationRegistry):
        self._station_registry = station_registry
        # Add any additional initialization here


    def add_line(self, name: str, station_ids: list[str]):
        """
        Adds a new line to the metro network with the given name and list of station IDs.
        The stations must already exist in the station registry. If any station ID does not exist, raises a ValueError.
        If the line name already exists, raises a ValueError.
        """
        raise NotImplementedError()

    def get_connected_stations(self, station_id: str) -> list[Station]:
        """
        Given a station ID, returns a list of Station objects that are directly connected to it and not closed.
        If the station ID does not exist, raises a ValueError.
        """
        raise NotImplementedError()

    def find_route(self, from_station_id: str, to_station_id: str, search_type: Literal["bfs", "dfs"] = "bfs") -> list[
        Station]:
        """
        Given two station IDs, finds a route between them using either BFS or DFS.
        Returns a list of Station objects representing the route. If no route exists, returns None.
        If either station ID does not exist, raises a ValueError.
        """
        raise NotImplementedError()

    def as_adjacency_list(self) -> dict[str, list[str]]:
        """
        Returns the state of the metro network as an adjacency list, where each key is a station ID and the
        value is a list of station IDs that are directly connected to it and not closed.
        """
        raise NotImplementedError()

    def as_adjacency_matrix(self) -> list[list[bool]]:
        """
        Returns the state of metro network as an adjacency matrix, where each row and column corresponds to a station.
        The index of each station is determined by the station registry, and can be reversed using the station registry.
        A value of True indicates a direct connection between the stations, while False indicates no direct connection or a closed segment.
        """
        raise NotImplementedError()


    def close_segment(self, from_station_id: str, to_station_id: str):
        """
        Temporarily closes the segment between two stations, preventing travel between them.
        If the segment is already closed or does not exist, raises a ValueError. 
        All methods that find routes or connected stations should respect the closed segments and not include them in their results.
        """
        raise NotImplementedError()

    def open_segment(self, from_station_id: str, to_station_id: str):
        """
        Reopens a previously closed segment between two stations, allowing travel between them.
        If the segment is not closed or does not exist, raises a ValueError.
        """
        raise NotImplementedError()

    def get_closed_segments(self) -> list[tuple[Station, Station]]:
        """
        Returns a list of tuples representing the closed segments in the metro network.
        Each tuple contains two Station objects representing the stations at either end of the closed segment.
        The returned segments are not available for travel and should not be included in any route or connected station queries.
        """
        raise NotImplementedError()


    def find_route_with_lines(self, from_station_id: str, to_station_id: str,
                              search_type: Literal["bfs", "dfs"] = "bfs") -> list[RouteSegment]:
        """
        Given two station IDs, finds a route between them using either BFS or DFS.
        Returns a list of RouteSegment objects representing the route, including the line used for each segment.
        If no route exists, returns None.
        If either station ID does not exist, raises a ValueError.
        """
        raise NotImplementedError()
