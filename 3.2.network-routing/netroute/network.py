from dataclasses import dataclass

from netroute.address import IPAddress
from netroute.registry import NetworkResolver
from netroute.routing_service import RoutingService


@dataclass
class Packet:
    """
    A message being transmitted through the network, with a TTL that limits how many hops it may traverse.
    """

    content: str
    source: IPAddress
    destination_address: IPAddress
    ttl: int

    def step(self) -> "Packet":
        """
        Decrement the TTL of the packet by 1 and return a new Packet instance.
        """
        return Packet(
            content=self.content,
            source=self.source,
            destination_address=self.destination_address,
            ttl=self.ttl - 1,
        )


@dataclass
class TransmissionResult:
    """
    The outcome of sending a packet through the network.
    """

    latency_ms: float
    dropped: bool


class Network:
    """
    Simulates packet transmission and route tracing across a resolved network topology.
    """

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
        Send ``packet`` from ``source`` to ``dest`` along the best route,
        decrementing TTL and accumulating link latency at each hop.

        :param source: The originating IP address.
        :param dest: The destination IP address.
        :param packet: The packet to send.
        :param timeout_ms: Maximum accumulated latency allowed before the packet is dropped.
        :return: The transmission result, including whether the packet was dropped and the latency incurred.
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
        Trace the route from ``source`` to ``dest``, hop by hop, until reaching
        ``dest`` or exceeding ``max_hops``/``timeout_ms``.

        :param source: The originating IP address.
        :param dest: The destination IP address.
        :param max_hops: Maximum number of links to traverse.
        :param timeout_ms: Maximum accumulated latency allowed.
        :return: A list of ``(address, latency)`` tuples along the path, starting
            with ``(source, 0.0)``. Empty if either endpoint is unknown; partial
            if the trace cannot reach ``dest``.
        """
        raise NotImplementedError()
