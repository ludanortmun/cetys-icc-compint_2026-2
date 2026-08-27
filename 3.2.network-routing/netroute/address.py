from typing import override


class IPAddress:
    __subnet_mask = 0b11111111111111111111111100000000  # /24 (255.255.255.0)

    @classmethod
    def subnets(cls):
        # start at 192.168.X.X
        return (IPAddress((192 << 24) | (168 << 16) | (i << 8)) for i in range(1, 255))

    def __init__(self, value: int):
        self.value: int = value

    @property
    def subnet_address(self) -> "IPAddress":
        return IPAddress(self.value & self.__subnet_mask)

    def is_same_subnet(self, other: "IPAddress") -> bool:
        return other.subnet_address == self.subnet_address

    def is_subnet(self) -> bool:
        return self.value & ~self.__subnet_mask == 0

    def address_space(self):
        """
        Returns a generator of all possible host addresses in the same subnet as this IP address.
        """
        subnet = self.subnet_address
        return (IPAddress(subnet.value | i) for i in range(1, 255))

    @classmethod
    def from_string(cls, ip_str: str) -> "IPAddress":
        parts = list(map(int, ip_str.split(".")))
        if len(parts) != 4 or any(part < 0 or part > 255 for part in parts):
            raise ValueError(f"Invalid IP address format: {ip_str}")
        value = (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]
        return cls(value)

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
