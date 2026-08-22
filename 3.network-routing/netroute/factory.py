import random

from netroute.host import Host
from netroute.network import IPAddress, NetworkDevice
from netroute.router import Router


def single_network(n_hosts: int) -> dict[IPAddress, NetworkDevice]:
    subnet = IPAddress.subnets().__next__()
    addresses = subnet.address_space()
    router = Router(
        address=addresses.__next__(),
        link_latency_ms=1.0,
    )
    hosts = [
        Host(ip, router, random.uniform(1.0, 10.0))
        for i, ip in enumerate(addresses)
        if i < n_hosts
    ]
    for h in hosts:
        router.add_host(h)

    return {router.address: router, **{h.address: h for h in hosts}}


def mobile_network(n_antennas: int, n_hosts: int) -> dict[IPAddress, NetworkDevice]:
    res: dict[IPAddress, NetworkDevice] = {}
    antennas: list[Router] = []
    for i, subnet in enumerate(IPAddress.subnets()):
        if i >= n_antennas:
            break

        addresses = subnet.address_space()
        router = Router(
            address=next(addresses),
            link_latency_ms=1.0,
        )
        res[router.address] = router
        antennas.append(router)

        hosts = [slow_host(ip, router) for i, ip in enumerate(addresses) if i < n_hosts]
        for h in hosts:
            router.add_host(h)
            res[h.address] = h

    # interconnect antennas
    for a in antennas:
        for b in antennas:
            if a.address != b.address:
                a.peer_with(b)

    return res


def slow_host(address: IPAddress, gateway: NetworkDevice) -> Host:
    return Host(address, gateway, random.uniform(100.0, 500.0))
