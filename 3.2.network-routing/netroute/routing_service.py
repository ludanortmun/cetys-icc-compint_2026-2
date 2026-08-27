from math import inf

from netroute.address import IPAddress
from netroute.client import Client
from netroute.registry import NetworkResolver
from netroute.routing import RoutingTable


class RoutingService:
    """Build and provide routing tables for a resolved network topology."""

    def __init__(self, resolver: NetworkResolver) -> None:
        self._resolver = resolver
        self._tables: dict[IPAddress, RoutingTable] | None = None

    def build(self) -> None:
        """
        Build all routing tables once, after the topology is complete.

        For each router, compute the best path to all other reachable subnets, minimizing the total latency.
        The next hop for each subnet is the first router along the best path.
        Additionally, each router's routing table will include direct routes to its own clients,
        and each client will have a default route to its gateway router.

        This method must be called explicitly and only once.
        """
        raise NotImplementedError()

    def get_for(self, address: IPAddress) -> RoutingTable:
        """
        Return the precomputed routing table for ``address`` in constant time.

        :raises RuntimeError: If routing tables have not been built.
        :raises ValueError: If ``address`` is unknown after a successful build.
        """
        raise NotImplementedError()