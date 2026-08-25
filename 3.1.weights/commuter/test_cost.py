from typing_extensions import override

from commuter.cost import TripDistanceCalculator, TripDurationCalculator
from commuter.roads import MapService


class StubMapService(MapService):
    """
    A stub MapService that serves hand-crafted distances (in meters) and
    speed limits (in km/h) instead of the real city data, so tests can
    reason about simple, predictable values.
    """

    def __init__(
        self,
        distances_map: dict[str, list[tuple[str, float]]],
        speed_limits_map: dict[str, list[tuple[str, float]]],
    ):
        self._distances_map = distances_map
        self._speed_limits_map = speed_limits_map

    @override
    def create_city_map(self):
        return {
            node: [dest for dest, _ in neighbors]
            for node, neighbors in self._distances_map.items()
        }

    @override
    def create_speed_limits_map(self):
        return {
            node: list(neighbors) for node, neighbors in self._speed_limits_map.items()
        }

    @override
    def create_distances_map(self):
        return {
            node: list(neighbors) for node, neighbors in self._distances_map.items()
        }


# Route: a -> b -> c
# a -> b: 1000 m at 60 km/h
# b -> c: 500 m at 30 km/h
DISTANCES_MAP = {
    "a": [("b", 1000)],
    "b": [("a", 1000), ("c", 500)],
    "c": [("b", 500)],
}

SPEED_LIMITS_MAP = {
    "a": [("b", 60)],
    "b": [("a", 60), ("c", 30)],
    "c": [("b", 30)],
}


def _make_map_service() -> StubMapService:
    return StubMapService(DISTANCES_MAP, SPEED_LIMITS_MAP)


def test_distance_calculator_converts_meters_to_km_for_single_leg():
    calculator = TripDistanceCalculator(_make_map_service())

    assert calculator.get_cost(["a", "b"]) == 1.0


def test_distance_calculator_sums_distances_across_multiple_legs():
    calculator = TripDistanceCalculator(_make_map_service())

    assert calculator.get_cost(["a", "b", "c"]) == 1.5


def test_distance_calculator_returns_zero_for_a_trivial_route():
    calculator = TripDistanceCalculator(_make_map_service())

    assert calculator.get_cost(["a"]) == 0.0


def test_duration_calculator_computes_minutes_for_single_leg():
    calculator = TripDurationCalculator(_make_map_service())

    # 1000m = 1km at 60km/h -> 1 minute
    assert calculator.get_cost(["a", "b"]) == 1.0


def test_duration_calculator_sums_durations_across_multiple_legs_with_different_speeds():
    calculator = TripDurationCalculator(_make_map_service())

    # a -> b: 1km at 60km/h -> 1 min
    # b -> c: 0.5km at 30km/h -> 1 min
    assert calculator.get_cost(["a", "b", "c"]) == 2.0


def test_duration_calculator_returns_zero_for_a_trivial_route():
    calculator = TripDurationCalculator(_make_map_service())

    assert calculator.get_cost(["a"]) == 0.0
