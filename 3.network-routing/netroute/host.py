from typing import override

from netroute.network import IPAddress, NetworkDevice, Packet


class Host(NetworkDevice):
    def __init__(
        self, address: IPAddress, gateway: NetworkDevice, link_latency_ms: float
    ) -> None:
        self._address: IPAddress = address
        self._gateway: NetworkDevice = gateway
        self._link_latency_ms: float = link_latency_ms

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
        A network host will always send packets to it's given gateway, regardless of the destination address.
        """
        print(f"+{self.link_latency_ms}ms")
        self._gateway.rx(packet)

    @override
    def rx(self, packet: Packet) -> None:
        """
        If a packet reached a Host, it should be it's final destination. If the packet's TTL is expired, it should be dropped.
        """
        p = packet.step()
        if p.ttl <= 0:
            print(f"[from {packet.source}] (dropped, TTL expired)")
        if p.destination_address != self.address:
            print(f"[from {packet.source}] (dropped, wrong destination)")

        else:
            print(f"[from {packet.source}] {packet.content}")
