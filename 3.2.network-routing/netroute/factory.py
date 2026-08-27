import math
import random
from collections.abc import Callable, Collection, Iterable
from itertools import combinations, islice
from numbers import Real

from netroute.address import IPAddress
from netroute.client import Client
from netroute.network import Network
from netroute.registry import DeviceRegistry
from netroute.router import Router
from netroute.routing_service import RoutingService

ClientFactory = Callable[[IPAddress, IPAddress, float], Client]
RouterFactory = Callable[[IPAddress, float], Router]

WIRED_CLIENT_LATENCY_RANGE: tuple[float, float] = (0.5, 2.0)
WIRELESS_CLIENT_LATENCY_RANGE: tuple[float, float] = (2.0, 10.0)
FIBER_ROUTER_LATENCY_RANGE: tuple[float, float] = (0.1, 1.0)
MOBILE_ROUTER_LATENCY_RANGE: tuple[float, float] = (5.0, 20.0)
SATELLITE_ROUTER_LATENCY_RANGE: tuple[float, float] = (250.0, 700.0)

RANDOM_HOST_COUNT_RANGE = (1, 8)


def _validate_latency(latency: float, name: str = "latency") -> float:
    if (isinstance(latency, bool) or not isinstance(latency, Real)
            or not math.isfinite(latency) or latency < 0):
        raise ValueError(f"{name} must be a finite, non-negative number")
    return float(latency)


def create_wired_client(
        address: IPAddress,
        gateway: IPAddress,
        latency: float,
) -> Client:
    """Create a wired client with an explicitly selected link latency."""
    return Client(address, gateway, _validate_latency(latency))


def create_wireless_client(
        address: IPAddress,
        gateway: IPAddress,
        latency: float,
) -> Client:
    """Create a wireless client with an explicitly selected link latency."""
    return Client(address, gateway, _validate_latency(latency))


def create_fiber_router(address: IPAddress, latency: float) -> Router:
    """Create a fiber router with an explicitly selected link latency."""
    return Router(address, _validate_latency(latency))


def create_mobile_router(address: IPAddress, latency: float) -> Router:
    """Create a 5G home router that can serve wired or wireless clients."""
    return Router(address, _validate_latency(latency))


def create_satellite_router(address: IPAddress, latency: float) -> Router:
    """Create a satellite router with an explicitly selected link latency."""
    return Router(address, _validate_latency(latency))


def create_subnet(
        registry: DeviceRegistry,
        router_address: IPAddress,
        n_hosts: int,
        router_factory: RouterFactory,
        client_factory: ClientFactory,
        router_latency: float,
        client_latencies: Iterable[float],
) -> tuple[Router, list[Client]]:
    """Create and register one router and its clients in ``registry``."""
    if isinstance(n_hosts, bool) or not isinstance(n_hosts, int) or n_hosts < 0:
        raise ValueError("n_hosts must be a non-negative integer")

    latencies = list(client_latencies)
    if len(latencies) != n_hosts:
        raise ValueError(
            f"Expected {n_hosts} client latencies, received {len(latencies)}"
        )
    router_latency = _validate_latency(router_latency, "router_latency")
    latencies = [
        _validate_latency(latency, f"client_latencies[{index}]")
        for index, latency in enumerate(latencies)
    ]

    address_space = list(router_address.address_space())
    if router_address not in address_space:
        raise ValueError(f"Router address {router_address} is not a usable host address")

    client_addresses = [
        address for address in address_space if address != router_address
    ]
    if n_hosts > len(client_addresses):
        raise ValueError(
            f"Subnet {router_address.subnet_address} has capacity for "
            f"{len(client_addresses)} clients, not {n_hosts}"
        )
    client_addresses = client_addresses[:n_hosts]

    addresses = [router_address, *client_addresses]
    occupied = [address for address in addresses if registry.resolve(address) is not None]
    if occupied:
        raise ValueError(f"Address is already registered: {occupied[0]}")
    existing_router = registry.get_router(router_address.subnet_address)
    if existing_router is not None:
        raise ValueError(
            f"A router is already registered for subnet "
            f"{router_address.subnet_address}"
        )

    router = router_factory(router_address, router_latency)
    clients = [
        client_factory(address, router_address, latency)
        for address, latency in zip(client_addresses, latencies, strict=True)
    ]
    if not isinstance(router, Router):
        raise TypeError("router_factory must return a Router")
    if router.address != router_address:
        raise ValueError("router_factory returned a router with the wrong address")
    if any(not isinstance(client, Client) for client in clients):
        raise TypeError("client_factory must return Client instances")
    if any(
            client.address != address or client.gateway != router_address
            for client, address in zip(clients, client_addresses, strict=True)
    ):
        raise ValueError(
            "client_factory returned a client with the wrong address or gateway"
        )

    router.with_clients([client.address for client in clients])
    registry.register(router)
    for client in clients:
        registry.register(client)
    return router, clients


def create_net(
        registry: DeviceRegistry,
        subnets: Iterable[tuple[Router, list[Client]]],
        peerings: Collection[tuple[IPAddress, IPAddress]],
) -> Network:
    """Peer registered subnet routers and return a fully built network."""
    subnet_list = list(subnets)
    routers = {router.address: router for router, _ in subnet_list}
    if len(routers) != len(subnet_list):
        raise ValueError("Each subnet must have a distinct router")

    for router, clients in subnet_list:
        if registry.resolve(router.address) is not router:
            raise ValueError(f"Router {router.address} is not registered")
        if registry.get_router(router.address.subnet_address) is not router:
            raise ValueError(
                f"Router {router.address} is not the registered subnet router"
            )
        for client in clients:
            if registry.resolve(client.address) is not client:
                raise ValueError(f"Client {client.address} is not registered")
            if client.gateway != router.address:
                raise ValueError(
                    f"Client {client.address} does not use router "
                    f"{router.address} as its gateway"
                )

    resolved_peerings: list[tuple[Router, Router]] = []
    for left_address, right_address in peerings:
        left = registry.resolve(left_address)
        right = registry.resolve(right_address)
        if not isinstance(left, Router) or left_address not in routers:
            raise ValueError(f"Unknown topology router: {left_address}")
        if not isinstance(right, Router) or right_address not in routers:
            raise ValueError(f"Unknown topology router: {right_address}")
        if left is right:
            raise ValueError(f"Router {left_address} cannot peer with itself")
        resolved_peerings.append((left, right))

    for left, right in resolved_peerings:
        left.with_peers([right.address])
        right.with_peers([left.address])

    routing_service = RoutingService(registry)
    routing_service.build()
    return Network(registry, routing_service)


def create_random_net(n_subnets: int) -> Network:
    """Create a random connected topology for interactive CLI use."""
    if (isinstance(n_subnets, bool) or not isinstance(n_subnets, int)
            or not 1 <= n_subnets <= 254):
        raise ValueError("n_subnets must be an integer between 1 and 254")

    registry = DeviceRegistry()
    subnet_addresses = list(islice(IPAddress.subnets(), n_subnets))
    router_options: tuple[
        tuple[RouterFactory, tuple[float, float], tuple[tuple[ClientFactory, tuple[float, float]], ...]],
        ...,
    ] = (
        (create_fiber_router, FIBER_ROUTER_LATENCY_RANGE,
         ((create_wired_client, WIRED_CLIENT_LATENCY_RANGE),)),
        (create_mobile_router, MOBILE_ROUTER_LATENCY_RANGE, (
            (create_wired_client, WIRED_CLIENT_LATENCY_RANGE),
            (create_wireless_client, WIRELESS_CLIENT_LATENCY_RANGE),
        )),
        (create_satellite_router, SATELLITE_ROUTER_LATENCY_RANGE,
         ((create_wireless_client, WIRELESS_CLIENT_LATENCY_RANGE),)),
    )

    subnets: list[tuple[Router, list[Client]]] = []
    for subnet_address in subnet_addresses:
        router_factory, router_range, client_options = random.choice(router_options)
        client_factory, client_range = random.choice(client_options)
        n_hosts = random.randint(*RANDOM_HOST_COUNT_RANGE)
        router_address = next(subnet_address.address_space())
        subnets.append(create_subnet(
            registry,
            router_address,
            n_hosts,
            router_factory,
            client_factory,
            random.uniform(*router_range),
            [random.uniform(*client_range) for _ in range(n_hosts)],
        ))

    router_addresses = [router.address for router, _ in subnets]
    peerings = list(zip(router_addresses, router_addresses[1:]))
    existing = {
        frozenset((left, right)) for left, right in peerings
    }
    for left, right in combinations(router_addresses, 2):
        edge = frozenset((left, right))
        if edge not in existing and random.random() < 0.25:
            peerings.append((left, right))

    return create_net(registry, subnets, peerings)
