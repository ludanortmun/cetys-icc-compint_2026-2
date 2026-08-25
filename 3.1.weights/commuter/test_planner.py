import itertools

import pytest
from typing_extensions import override

from commuter.cost import TripCostCalculator
from commuter.planner import TripPlanner
from commuter.roads import MapService


class StubMapService(MapService):
    """
    A stub MapService that serves a small, hand-crafted graph instead of the
    real city map, so tests can reason about simple, predictable topologies.
    """

    def __init__(self, city_map: dict[str, list[str]]):  # pyright: ignore[reportMissingSuperCall]
        self._city_map = city_map

    @override
    def create_city_map(self):
        return {node: list(neighbors) for node, neighbors in self._city_map.items()}

    @override
    def create_speed_limits_map(self):
        return {
            node: [(neighbor, 30) for neighbor in neighbors]
            for node, neighbors in self._city_map.items()
        }

    @override
    def create_distances_map(self):
        return {
            node: [(neighbor, 100) for neighbor in neighbors]
            for node, neighbors in self._city_map.items()
        }


class StubCostCalculator(TripCostCalculator):
    """
    A stub cost calculator whose cost is simply the number of hops in the
    route, avoiding any dependency on the real distance/duration logic.
    """

    @override
    def get_cost(self, route: list[str]) -> float:
        return float(len(route) - 1)


def _is_connected_route(city_map: dict[str, list[str]], route: list[str]) -> bool:
    """
    Verifies that every consecutive pair of nodes in the route is a valid
    edge in the given city map.
    """
    if not route:
        return False

    for source, dest in itertools.pairwise(route):
        if dest not in city_map.get(source, []):
            return False

    return True


# A connected linear graph: a - b - c - d
CONNECTED_MAP = {
    "a": ["b"],
    "b": ["a", "c"],
    "c": ["b", "d"],
    "d": ["c"],
}

# Two disconnected components: a - b, and c - d
DISCONNECTED_MAP = {
    "a": ["b"],
    "b": ["a"],
    "c": ["d"],
    "d": ["c"],
}


def _make_planner(city_map: dict[str, list[str]]) -> TripPlanner:
    map_service = StubMapService(city_map)
    return TripPlanner(map_service, StubCostCalculator())


def test_raises_value_error_when_origin_not_in_graph():
    planner = _make_planner(CONNECTED_MAP)

    with pytest.raises(ValueError):
        planner.plan_route("z", "a")


def test_raises_value_error_when_destination_not_in_graph():
    planner = _make_planner(CONNECTED_MAP)

    with pytest.raises(ValueError):
        planner.plan_route("a", "z")


def test_raises_value_error_when_no_path_exists_between_origin_and_destination():
    planner = _make_planner(DISCONNECTED_MAP)

    with pytest.raises(ValueError):
        planner.plan_route("a", "c")


def test_returned_route_starts_at_origin_and_ends_at_destination():
    planner = _make_planner(CONNECTED_MAP)

    plan = planner.plan_route("a", "d")

    assert plan.route[0] == "a"
    assert plan.route[-1] == "d"


def test_returned_route_is_a_valid_path_in_the_graph():
    planner = _make_planner(CONNECTED_MAP)

    plan = planner.plan_route("a", "d")

    assert _is_connected_route(CONNECTED_MAP, plan.route)


def test_returned_route_between_same_origin_and_destination_is_trivial():
    planner = _make_planner(CONNECTED_MAP)

    plan = planner.plan_route("a", "a")

    assert plan.route == ["a"]
