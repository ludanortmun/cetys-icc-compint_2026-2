from abc import ABC, abstractmethod
from typing import override

from netroute.address import IPAddress
from netroute.device import Device


class DeviceResolver(ABC):
    """
    Defines an interface for resolving devices based on their IP addresses.
    """
    @abstractmethod
    def resolve(self, address: IPAddress) -> Device | None:
        """
        Resolve a device based on its IP address.
        :param address: The IP address of the device to resolve.
        :return: The device corresponding to the given IP address, or None if not found.
        """
        raise NotImplementedError()


class DeviceRegistry(DeviceResolver):
    """
    A concrete implementation of DeviceResolver that maintains a registry of devices.
    It allows registering devices and resolving them based on their IP addresses.
    """
    def __init__(self):
        self._devices: dict[IPAddress, Device] = {}

    def register(self, device: Device) -> None:
        """
        Add a device to the registry.
        :param device: The device to register.
        :return: None
        """
        self._devices[device.address] = device

    @override
    def resolve(self, address: IPAddress) -> Device | None:
        """
        Resolve a device based on its IP address.
        :param address: The IP address of the device to resolve.
        :return: The device corresponding to the given IP address, or None if not found.
        """
        return self._devices.get(address)
