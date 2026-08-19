from dataclasses import dataclass
from typing import Literal

from metro.station import Station, StationRegistry


@dataclass()
class JourneyLeg:
    """
    Represents a portion of a journey between two stations on a specific line. 
    Each leg includes the line name, the boarding station ID, and the exit station ID.
    """
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
        Station] | None:
        """
        Given two station IDs, finds a route between them using either BFS or DFS.
        Returns a list of Station objects representing the route. If no route exists, returns None.
        If either station ID does not exist, raises a ValueError.
        If both station IDs are the same, raises a ValueError.
        """
        raise NotImplementedError()

    def as_adjacency_list(self) -> dict[str, list[str]]:
        """
        Returns the state of the metro network as an adjacency list, where each key is a station ID and the
        value is a list of station IDs that are directly connected to it and not closed.
        If a line exists in the station registry but does not belong to any line in the metro network, 
        it should appear in the adjacency list.
        """
        raise NotImplementedError()

    def as_adjacency_matrix(self) -> list[list[bool]]:
        """
        Returns the state of metro network as an adjacency matrix, where each row and column corresponds to a station.
        The index of each station is determined by the station registry, and can be reversed using the station registry.
        A value of True indicates a direct connection between the stations, while False indicates no direct connection or a closed segment.
        Dimensions of the matrix are determined by the number of stations in the station registry.
        """
        raise NotImplementedError()


    def close_segment(self, from_station_id: str, to_station_id: str):
        """
        Temporarily closes the segment between two stations, preventing travel between them.
        This is not bi-directional; closing a segment from A to B does not automatically close the segment from B to A.
        This is analogous to removing an edge from the graph representation of the metro network. 
        from_station_id and to_station_id must be valid and be contiguously connected in the network.
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


    def plan_journey(self, from_station_id: str, to_station_id: str,
                              search_type: Literal["bfs", "dfs"] = "bfs") -> list[JourneyLeg] | None:
        """
        Given two station IDs, finds a route between them using either BFS or DFS.
        Returns a list of JourneyLeg objects representing a portion of the trip.
        If no route exists, returns None.
        If either station ID does not exist, raises a ValueError.
        If both station IDs are the same, raises a ValueError.
        This method doesn't guarantee that the route is the shortest or the one with the fewest line changes.
        """
        # Tip: You can call self.find_route to get the list of stations, 
        #      and then convert that into a list of JourneyLeg objects 
        #      by checking which lines connect each pair of stations in the route.
        raise NotImplementedError()
