from typing import Collection, override

from netroute.device import Device
from netroute.address import IPAddress
from netroute.registry import DeviceResolver
from netroute.routing import RoutingTable


class Router(Device):
    def __init__(self, address: IPAddress, link_latency: float, resolver: DeviceResolver):
        self._address = address
        self._link_latency = link_latency
        self._resolver = resolver
        self._peers: set[IPAddress] = set()
        self._clients: set[IPAddress] = set()

    @property
    @override
    def address(self) -> IPAddress:
        """
        Return the IP address of the device.
        """
        return self._address

    @property
    def peers(self) -> frozenset[IPAddress]:
        return frozenset(self._peers)

    @property
    def clients(self) -> frozenset[IPAddress]:
        return frozenset(self._clients)

    @override
    def get_routing_table(self) -> RoutingTable:
        """
        Builds and returns the routing table of the device.
        A router's routing table includes entries for each of its clients and for
        each of its peers' subnets, with the next hop being the respective client or peer address.
        """
        raise NotImplementedError()

    @override
    def get_link_latency(self) -> float:
        """
        Return the link latency of the device, in milliseconds.
        """
        return self._link_latency

    def with_peers(self, others: Collection[IPAddress]) -> "Router":
        """
        Establish a peering relationship with multiple routers.
        """
        for other in others:
            if other not in self._peers:
                self._peers.add(other)

        return self

    def with_clients(self, clients: Collection[IPAddress]) -> "Router":
        """
        Establish a connection with multiple clients.
        """
        for client in clients:
            if client not in self._clients:
                self._clients.add(client)

        return self
