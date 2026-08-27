from dataclasses import dataclass

from netroute.address import IPAddress
from netroute.registry import NetworkResolver
from netroute.routing_service import RoutingService


@dataclass
class Packet:
    content: str
    source: IPAddress
    destination_address: IPAddress
    ttl: int

    def step(self) -> "Packet":
        """Decrement the TTL of the packet by 1 and return a new Packet instance."""
        return Packet(
            content=self.content,
            source=self.source,
            destination_address=self.destination_address,
            ttl=self.ttl - 1,
        )


@dataclass
class TransmissionResult:
    latency_ms: float
    dropped: bool


class Network:

    def __init__(
            self,
            resolver: NetworkResolver,
            routing_service: RoutingService,
    ) -> None:
        self._resolver: NetworkResolver = resolver
        self._routing_service: RoutingService = routing_service

    def send(
            self,
            source: IPAddress,
            dest: IPAddress,
            packet: Packet,
            timeout_ms: float = 1000.0,
    ) -> TransmissionResult:
        """
        Send ``packet`` from ``source`` to ``dest`` using the best route.

        At each device in the path, obtain the next address based on the routing table.
        Traversing that link costs the sum of the current and next devices' link latencies.
        TTL counts traversed links, so the source consumes no TTL and arrival
        at the destination with TTL exactly zero succeeds. Likewise, arrival
        at exactly ``timeout_ms`` succeeds; only a negative TTL or accumulated
        latency greater than ``timeout_ms`` drops the packet.

        Return ``TransmissionResult(total_latency, False)`` on delivery, where
        ``total_latency`` is the sum of the link latencies in the path.
        If either endpoint is unknown, no next hop exists, a next-hop address cannot be resolved, or
        ``total_latency`` exceeds ``timeout_ms``, return a dropped result.

        Any dropped result should preserve the accumulated latency up to the point of failure, which may be zero.
        """
        raise NotImplementedError()

    def trace(
            self,
            source: IPAddress,
            dest: IPAddress,
            max_hops: int = 64,
            timeout_ms: float = 1000.0,
    ) -> list[tuple[IPAddress, float]]:
        """
        Trace the network route from ``source`` to ``dest``.

        Begin with ``(source, 0.0)`` and find every next address with
        ``routing_service.get_for(current).next_hop(dest)``. Each subsequent
        tuple contains the reached address and the latency introduced by that hop.
        ``max_hops`` counts links rather than entries, so the source consumes
        no hop. Reaching the destination using exactly ``max_hops`` or at
        exactly ``timeout_ms`` is allowed; stop only before a link would
        exceed either budget.

        Return an empty list when either endpoint is unknown. If no next hop
        exists or a next-hop address cannot be resolved, return the partial
        trace through the last reached device.
        """
        raise NotImplementedError()
