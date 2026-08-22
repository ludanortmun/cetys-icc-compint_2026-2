from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import override


class IPAddress:
    __subnet_mask = 0b11111111111111111111111100000000  # /24 (255.255.255.0)

    @classmethod
    def subnets(cls):
        # start at 192.168.X.X
        return (IPAddress((192 << 24) | (168 << 16) | (i << 8)) for i in range(1, 255))

    def __init__(self, value: int):
        self.value: int = value

    def subnet_address(self) -> int:
        return self.value & self.__subnet_mask

    def is_same_subnet(self, other: "IPAddress") -> bool:
        return other.subnet_address() == self.subnet_address()

    def address_space(self):
        """
        Returns a generator of all possible host addresses in the same subnet as this IP address.
        """
        subnet = self.subnet_address()
        return (IPAddress(subnet | i) for i in range(1, 255))

    @override
    def __hash__(self) -> int:
        return hash(self.value)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPAddress):
            return NotImplemented
        return self.value == other.value

    @override
    def __repr__(self) -> str:
        return f"{self.value >> 24 & 0xFF}.{self.value >> 16 & 0xFF}.{self.value >> 8 & 0xFF}.{self.value & 0xFF}"


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
            ttl=self.ttl - 1
        )


class NetworkDevice(ABC):
    @property
    @abstractmethod
    def address(self) -> IPAddress:
        """
        IP address of the device.
        """

    @property
    @abstractmethod
    def link_latency_ms(self) -> float:
        """
        Returns the network latency (in miliseconds) introduces by this device.
        Total latency of a packet is the sum of the latencies of all devices in the path.
        """


    @abstractmethod
    def tx(self, packet: Packet) -> None:
        """
        Transmit a packet to the next device in the path.
        """


    @abstractmethod
    def rx(self, packet: Packet) -> None:
        """
        Receive a packet from another device in the network.
        """
