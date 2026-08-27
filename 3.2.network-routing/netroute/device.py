from abc import ABC, abstractmethod

from netroute.address import IPAddress
from netroute.routing import RoutingTable


class Device(ABC):
    @property
    @abstractmethod
    def address(self) -> IPAddress:
        """
        Return the IP address of the device.
        """

    @abstractmethod
    def get_routing_table(self) -> RoutingTable:
        """
        Builds and returns the routing table of the device.
        """

    @abstractmethod
    def get_link_latency(self) -> float:
        """
        Return the link latency of the device, in milliseconds.
        """
