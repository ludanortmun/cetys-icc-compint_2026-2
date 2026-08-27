from typing import override

from netroute.address import IPAddress
from netroute.device import Device


class Client(Device):
    """
    Represents a client device in the network.
    """

    def __init__(self, address: IPAddress, gateway: IPAddress,
                 link_latency: float):
        self._address = address
        self._gateway = gateway
        self._link_latency = link_latency

    @property
    @override
    def address(self) -> IPAddress:
        """
        Return the IP address of the device.
        """
        return self._address

    @property
    def gateway(self) -> IPAddress:
        return self._gateway

    @override
    def get_link_latency(self) -> float:
        """
        Return the link latency of the device, in milliseconds.
        """
        return self._link_latency
