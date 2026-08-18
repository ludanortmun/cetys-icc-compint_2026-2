from dataclasses import dataclass
from collections.abc import Iterable


@dataclass(frozen=True)
class Station:
    id: str
    name: str


class StationRegistry:
    """
    Source of truth for all stations in the metro network. Provides methods to add, retrieve, and list stations, as well as to convert between station IDs and their corresponding indexes.
    This class is designed to be used by the MetroNetwork class to manage station data.
    """

    @classmethod
    def from_stations(cls, stations: Iterable[Station]) -> "StationRegistry":
        """
        Creates a StationRegistry from a collection of Station objects.
        """
        registry = cls()
        for station in stations:
            registry.add_station(station)
        return registry

    def __init__(self):
        self._stations: dict[str, Station] = {}
        self._idx_to_id: dict[int, str] = {}
        self._id_to_idx: dict[str, int] = {}

    def add_station(self, station: Station):
        """
        Adds a new station to the registry. If a station with the same ID already exists, raises a ValueError.
        """
        if station.id in self._stations:
            raise ValueError(f"Station with ID {station.id} already exists.")
        self._stations[station.id] = station
        self._id_to_idx[station.id] = len(self._id_to_idx)
        self._idx_to_id[len(self._idx_to_id)] = station.id

    def get_station(self, station_id: str) -> Station:
        """
        Retrieves a station by its ID. If the station does not exist, raises a ValueError.
        """
        if station_id not in self._stations:
            raise ValueError(f"Station with ID {station_id} does not exist.")
        return self._stations[station_id]

    def all_stations(self) -> list[Station]:
        """
        Returns a list of all stations in the registry.
        """
        return list(self._stations.values())

    def idx_to_id(self, index: int) -> str:
        """
        Given an index, returns the corresponding station ID. If the index is out of bounds, raises an IndexError.
        """
        if index not in self._idx_to_id:
            raise IndexError("Index out of bounds.")
        return self._idx_to_id[index]

    def id_to_idx(self, station_id: str) -> int:
        """
        Given a station ID, returns its index in the registry. If the station does not exist, raises a ValueError.
        """
        if station_id not in self._id_to_idx:
            raise ValueError(f"Station with ID {station_id} does not exist.")
        return self._id_to_idx[station_id]
