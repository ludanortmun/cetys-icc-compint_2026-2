import copy
from itertools import product

_h_streets = [chr(c) for c in range(ord("a"), ord("g") + 1)]
_v_streets = [i for i in range(1, 8)]

# Manually designed intersections that do not exist in the city.
_non_existent = ["d2", "d4", "d6"]
# Special cases for Diamond longer blocks
_long_blocks = [("d1", "d3"), ("d3", "d5"), ("d5", "d7")]
# Exit ramps on Diamond and on 7th.
_ramps = ["xd", "x7"]
_speed_limits = {"local": 15, "collectors": 40, "arterial": 80}

_collectors = {"d", 3, 7}


class MapService:
    def __init__(self):
        self._adj_list: dict[str, list[str]] = self._build_adj_list()

    def create_city_map(self) -> dict[str, list[str]]:
        """
        Returns the map of Cherry Hills, represented as an adjacency list
        where each node is a junction and each edge is a road connecting two junctions.
        """
        return copy.deepcopy(self._adj_list)

    def create_speed_limits_map(self) -> dict[str, list[tuple[str, int]]]:
        """
        Returns the map of Cherry Hills, represented as an adjacency list
        where each node is a junction and each edge is a road connecting two junctions,
        along with the speed limit for each road. Speeds are expressed in km/h.
        """
        speed_limits_map = {
            s: [(d, self._get_speed_limit(s, d)) for d in dests]
            for s, dests in self._adj_list.items()
        }
        return copy.deepcopy(speed_limits_map)

    def create_distances_map(self) -> dict[str, list[tuple[str, int]]]:
        """
        Returns the map of Cherry Hills, represented as an adjacency list
        where each node is a junction and each edge is a road connecting two junctions,
        along with the distance for each road. Distances are expressed in meters.
        """
        distances_map = {
            s: [(d, self._get_distance(s, d)) for d in dests]
            for s, dests in self._adj_list.items()
        }
        return copy.deepcopy(distances_map)

    def _build_adj_list(self):
        adj_list = {
            self._to_intersection_name(pair[0], pair[1]): self._get_neighbors(
                pair[0], pair[1]
            )
            for pair in product(_h_streets, _v_streets)
            if self._to_intersection_name(pair[0], pair[1]) not in _non_existent
        }

        # Add ramps
        adj_list["d1"].append("xd")
        adj_list["g7"].append("x7")
        adj_list["xd"] = ["d1", "x7"]
        adj_list["x7"] = ["g7", "xd"]

        return adj_list

    def _to_intersection_name(self, x: str, y: int) -> str:
        return f"{x}{y}"

    def _get_neighbors(self, x: str, y: int) -> list[str]:
        neighbors: list[str] = []

        _x = ord(x) - ord("a")
        if _x > 0:
            neighbors.append(self._to_intersection_name(_h_streets[_x - 1], y))
        if _x < len(_h_streets) - 1:
            neighbors.append(self._to_intersection_name(_h_streets[_x + 1], y))
        if y > 1:
            neighbors.append(self._to_intersection_name(x, y - 1))
        if y < len(_v_streets):
            neighbors.append(self._to_intersection_name(x, y + 1))

        # Manual overrides for long blocks on Diamond
        if (x, y) == ("d", 1):
            neighbors.append(self._to_intersection_name("d", 3))
        if (x, y) == ("d", 3):
            neighbors.append(self._to_intersection_name("d", 1))
            neighbors.append(self._to_intersection_name("d", 5))
        if (x, y) == ("d", 5):
            neighbors.append(self._to_intersection_name("d", 3))
            neighbors.append(self._to_intersection_name("d", 7))
        if (x, y) == ("d", 7):
            neighbors.append(self._to_intersection_name("d", 5))

        return [n for n in neighbors if n not in _non_existent]

    def _get_speed_limit(self, source: str, dest: str):
        limit = _speed_limits["local"]

        # Override if currently driving on a collector
        if any(str(s) in source for s in _collectors) and any(
            str(d) in dest for d in _collectors
        ):
            limit = _speed_limits["collectors"]

        # Arterial overrides
        if "x" in source:
            limit = (
                _speed_limits["arterial"]
                if "x" in dest
                else _speed_limits["collectors"]
            )

        return limit

    def _get_distance(self, source: str, dest: str) -> int:
        # From 1 arterial exit to the next
        if "x" in source and "x" in dest:
            return 10000  # 1km
        elif ((source, dest) in _long_blocks) or ((dest, source) in _long_blocks):
            return 1000

        return 500
