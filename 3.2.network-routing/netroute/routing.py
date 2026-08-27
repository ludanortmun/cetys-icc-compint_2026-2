from netroute.address import IPAddress


class RoutingTable:
    """
    Maps destination addresses to their next hop for a single device.
    """

    def __init__(self, routes: dict[IPAddress, IPAddress] | None = None,
                 default: IPAddress | None = None):
        self._routes = dict(routes or {})
        self._default = default

    def set_route(self, dest: IPAddress, next_hop: IPAddress) -> "RoutingTable":
        """
        Adds a route to the routing table. If the destination address already exists, it will be updated with the new next hop.

        :param dest: The destination IP address.
        :param next_hop: The device IP address of the next hop.
        :return: The updated RoutingTable instance.
        :raises ValueError: If the next hop IP address is a subnet address.
        """
        if next_hop.is_subnet():
            raise ValueError(f"Next hop {next_hop} cannot be a subnet address.")

        self._routes[dest] = next_hop
        return self

    def next_hop(self, dest: IPAddress) -> IPAddress | None:
        """
        Finds the next hop for a given destination address.
        If the destination address is not found in the routing table, it will check for the subnet address.
        If neither is found, it will return the default route if it exists.

        :param dest: The destination IP address.
        :return: The IP address of the next hop, or None if no route is found.
        """
        return (self._routes.get(dest)
                or self._routes.get(dest.subnet_address)
                or self._default)
