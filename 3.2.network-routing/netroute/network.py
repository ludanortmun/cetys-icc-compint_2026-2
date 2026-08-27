from dataclasses import dataclass

from netroute.address import IPAddress
from netroute.registry import DeviceRegistry


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

    def __init__(self, registry: DeviceRegistry) -> None:
        self._registry = registry

    def send(
            self,
            source: IPAddress,
            dest: IPAddress,
            packet: Packet,
            timeout_ms: float = 1000.0,
    ) -> TransmissionResult:
        """
        Send a packet from source to destination.
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
        Trace the route from source to destination.
        Stops if the hop count exceeds max_hops or the accumulated latency exceeds timeout_ms.
        :returns: A list of tuples containing the IP address of each hop and the latency introduced by that hop.
        """
        raise NotImplementedError()
