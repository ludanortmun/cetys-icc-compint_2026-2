from typing import override

from netroute.host import Host
from netroute.network import IPAddress, NetworkDevice, Packet


class Router(NetworkDevice):
    def __init__(
        self,
        address: IPAddress,
        link_latency_ms: float,
    ) -> None:
        self._address: IPAddress = address
        self._link_latency_ms: float = link_latency_ms
        self._hosts: list[Host] = []
        self._peers: list[Router] = []

    def add_host(self, host: Host) -> None:
        self._hosts.append(host)

    def peer_with(self, router: "Router") -> None:
        self._peers.append(router)
        router._peers.append(self)

    @property
    @override
    def address(self) -> IPAddress:
        return self._address

    @property
    @override
    def link_latency_ms(self) -> float:
        return self._link_latency_ms

    @override
    def tx(self, packet: Packet) -> None:
        """
        Sends the Packet to the next device (either a Host or another Router) based on the destination address of the packet.
        If the destination address is in the same subnet, it should be sent to the corresponding Host.
        Otherwise, it should be sent to the next Router in the path.
        """

    @override
    def rx(self, packet: Packet) -> None:
        """
        When a Router receieves a Packet, it should:
            - Decrement TTL for the packet and check if it has expired. If so, drop the packet and print a message.
            - Transmit the packet to the next hop (either a Host or another Router) based on the destination address of the packet.
        """

    def routing_table(self):
        """
        Returns a dictionary mapping destination IP addresses to the next hop (either a Host or another Router).
        The routing table must include all Hosts in the same subnet and all peered Routers.
        """
        r = {}
        for h in self._hosts:
            r[h.address] = h.link_latency_ms + self.link_latency_ms
        for p in self._peers:
            r[p.address] = p.link_latency_ms + self.link_latency_ms

        return r
