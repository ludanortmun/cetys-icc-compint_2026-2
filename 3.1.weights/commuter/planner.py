from dataclasses import dataclass
from pprint import pprint

from commuter.cost import TripCostCalculator
from commuter.roads import MapService


@dataclass
class Plan:
    route: list[str]
    cost: float


class TripPlanner:
    def __init__(self, map_service: MapService, cost_calculator: TripCostCalculator):
        self.map_service: MapService = map_service
        self.cost_calculator: TripCostCalculator = cost_calculator

    def plan_route(self, origin: str, destination: str) -> Plan:
        """
        Plans a route from the origin to the destination and returns a Plan object
        containing the route and its associated cost.
        Raises a ValueError if no route is found between the origin and destination.
        """
        raise NotImplementedError()
