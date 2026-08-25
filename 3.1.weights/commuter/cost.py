from abc import ABC, abstractmethod

from typing_extensions import override

from commuter.roads import MapService


class TripCostCalculator(ABC):
    @abstractmethod
    def get_cost(self, route: list[str]) -> float:
        """
        Calculates the cost of a trip based on the provided route.
        """


class TripDistanceCalculator(TripCostCalculator):
    """
    Computes the cost of a trip expressed in the total distance traveled.
    """

    def __init__(self, map_service: MapService):
        self.map_service: MapService = map_service

    @override
    def get_cost(self, route: list[str]) -> float:
        """
        Calculates the total distance of the trip based on the provided route.
        Distance is presented in km.
        Raises ValueError if there is no distance defined for a road in the route.
        """
        raise NotImplementedError()


class TripDurationCalculator(TripCostCalculator):
    """
    Computes the cost of a trip expressed in the total duration of the trip.
    """

    def __init__(self, map_service: MapService):
        self.map_service: MapService = map_service

    @override
    def get_cost(self, route: list[str]) -> float:
        """
        Calculates the total duration of the trip based on the provided route.
        Duration is presented in minutes.
        Raises ValueError if there is no speed limit and distance defined for a road in the route.
        """
        raise NotImplementedError()
