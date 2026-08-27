from netroute.address import IPAddress
from netroute.registry import NetworkResolver
from netroute.routing import RoutingTable


class RoutingService:
    """
    Build and provide routing tables for a resolved network topology.
    """

    def __init__(self, resolver: NetworkResolver) -> None:
        self._resolver = resolver
        self._tables: dict[IPAddress, RoutingTable] | None = None

    def build(self) -> None:
        """
        Compute routing tables for every router, minimizing total latency,
        plus direct routes to each router's clients and a default route for
        each client to its gateway router.

        Must be called explicitly, exactly once, before ``get_for``.
        """
        raise NotImplementedError()

    def get_for(self, address: IPAddress) -> RoutingTable:
        """
        Return the precomputed routing table for ``address`` in constant time.

        :raises RuntimeError: If routing tables have not been built.
        :raises ValueError: If ``address`` is unknown after a successful build.
        """
        raise NotImplementedError()
