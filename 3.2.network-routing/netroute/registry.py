from abc import ABC, abstractmethod
from typing import override

from netroute.address import IPAddress
from netroute.device import Device
from netroute.router import Router


class NetworkResolver(ABC):
    """
    Defines an interface for resolving devices and routers in a network.
    """

    @abstractmethod
    def resolve(self, address: IPAddress) -> Device | None:
        """
        Resolve a device based on its IP address.
        :param address: The IP address of the device to resolve.
        :return: The device corresponding to the given IP address, or None if not found.
        """

    @abstractmethod
    def get_router(self, subnet: IPAddress) -> Router | None:
        """
        Return the router registered for a subnet, if any.
        """

    @abstractmethod
    def get_subnets(self) -> frozenset[IPAddress]:
        """
        Return the subnets that have a registered router.
        """


class DeviceRegistry(NetworkResolver):
    """
    Maintains address-to-device and subnet-to-router indexes for a network.
    """

    def __init__(self) -> None:
        self._devices: dict[IPAddress, Device] = {}
        self._routers: dict[IPAddress, Router] = {}

    def register(self, device: Device) -> None:
        """
        Add a device to the registry.
        :param device: The device to register.
        :return: None
        """
        existing_device = self._devices.get(device.address)
        if existing_device is device:
            return
        if existing_device is not None:
            raise ValueError(f"Address is already registered: {device.address}")

        if isinstance(device, Router):
            subnet = device.address.subnet_address
            existing_router = self._routers.get(subnet)
            if existing_router is not None and existing_router is not device:
                raise ValueError(f"A router is already registered for subnet {subnet}")
            self._routers[subnet] = device

        self._devices[device.address] = device

    @override
    def resolve(self, address: IPAddress) -> Device | None:
        """
        Resolve a device based on its IP address.
        :param address: The IP address of the device to resolve.
        :return: The device corresponding to the given IP address, or None if not found.
        """
        return self._devices.get(address)

    @override
    def get_router(self, subnet: IPAddress) -> Router | None:
        """
        Return the router registered for a subnet, if any.
        """
        return self._routers.get(subnet.subnet_address)

    @override
    def get_subnets(self) -> frozenset[IPAddress]:
        """
        Return the subnets that have a registered router.
        """
        return frozenset(self._routers)
