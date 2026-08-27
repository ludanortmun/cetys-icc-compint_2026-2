from abc import ABC, abstractmethod

from netroute.address import IPAddress


class Device(ABC):
    @property
    @abstractmethod
    def address(self) -> IPAddress:
        """
        Return the IP address of the device.
        """

    @abstractmethod
    def get_link_latency(self) -> float:
        """
        Return the link latency of the device, in milliseconds.
        """
