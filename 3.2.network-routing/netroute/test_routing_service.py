"""Checklist-style grading tests for RoutingService (50 points)."""

import pytest

from netroute.address import IPAddress
from netroute.factory import (
    create_fiber_router,
    create_subnet,
    create_wired_client,
)
from netroute.registry import DeviceRegistry
from netroute.routing_service import RoutingService


def ip(value: str) -> IPAddress:
    return IPAddress.from_string(value)


def subnet(
    registry: DeviceRegistry,
    router_address: str,
    router_latency: float,
    client_latencies: list[float],
):
    return create_subnet(
        registry,
        ip(router_address),
        len(client_latencies),
        create_fiber_router,
        create_wired_client,
        router_latency,
        client_latencies,
    )


def peer(left, right) -> None:
    left.with_peers([right.address])
    right.with_peers([left.address])


class TestRoutingServiceBuild:
    """40 points: build creates complete, cheapest deterministic routes."""

    def test_build_adds_direct_client_and_default_gateway_routes(self) -> None:
        registry = DeviceRegistry()
        router, clients = subnet(registry, "192.168.1.1", 1.0, [2.0])
        service = RoutingService(registry)

        service.build()

        assert service.get_for(router.address).next_hop(clients[0].address) == clients[0].address
        assert service.get_for(clients[0].address).next_hop(ip("192.168.9.9")) == router.address

    def test_build_routes_multiple_clients_in_one_subnet(self) -> None:
        registry = DeviceRegistry()
        router, clients = subnet(registry, "192.168.1.1", 1.0, [2.0, 3.0, 4.0])
        service = RoutingService(registry)

        service.build()

        table = service.get_for(router.address)
        assert [table.next_hop(client.address) for client in clients] == [
            client.address for client in clients
        ]

    def test_build_adds_direct_peer_and_remote_subnet_routes(self) -> None:
        registry = DeviceRegistry()
        left, _ = subnet(registry, "192.168.1.1", 1.0, [2.0])
        right, right_clients = subnet(registry, "192.168.2.1", 3.0, [4.0])
        peer(left, right)
        service = RoutingService(registry)

        service.build()

        table = service.get_for(left.address)
        assert table.next_hop(right.address) == right.address
        assert table.next_hop(right_clients[0].address) == right.address

    def test_build_routes_bidirectionally_across_a_b_c(self) -> None:
        registry = DeviceRegistry()
        router_a, clients_a = subnet(registry, "192.168.1.1", 1.0, [2.0])
        router_b, _ = subnet(registry, "192.168.2.1", 3.0, [4.0])
        router_c, clients_c = subnet(registry, "192.168.3.1", 5.0, [6.0])
        peer(router_a, router_b)
        peer(router_b, router_c)
        service = RoutingService(registry)

        service.build()

        assert service.get_for(router_a.address).next_hop(clients_c[0].address) == router_b.address
        assert service.get_for(router_c.address).next_hop(clients_a[0].address) == router_b.address

    def test_build_leaves_a_disconnected_subnet_unroutable(self) -> None:
        registry = DeviceRegistry()
        connected, _ = subnet(registry, "192.168.1.1", 1.0, [2.0])
        isolated, isolated_clients = subnet(registry, "192.168.2.1", 3.0, [4.0])
        service = RoutingService(registry)

        service.build()

        assert service.get_for(connected.address).next_hop(isolated.address) is None
        assert service.get_for(connected.address).next_hop(isolated_clients[0].address) is None

    def test_build_chooses_the_lower_latency_competing_path(self) -> None:
        registry = DeviceRegistry()
        start, _ = subnet(registry, "192.168.1.1", 10.0, [])
        slow, _ = subnet(registry, "192.168.2.1", 8.0, [])
        fast, _ = subnet(registry, "192.168.3.1", 2.0, [])
        finish, finish_clients = subnet(registry, "192.168.4.1", 6.0, [1.0])
        peer(start, slow)
        peer(slow, finish)
        peer(start, fast)
        peer(fast, finish)
        service = RoutingService(registry)

        service.build()

        # (10 + 2) + (2 + 6) beats (10 + 8) + (8 + 6).
        assert service.get_for(start.address).next_hop(finish_clients[0].address) == fast.address

    def test_build_breaks_equal_cost_ties_by_lowest_next_hop_ip(self) -> None:
        registry = DeviceRegistry()
        start, _ = subnet(registry, "192.168.1.1", 1.0, [])
        lower_ip, _ = subnet(registry, "192.168.2.1", 3.0, [])
        higher_ip, _ = subnet(registry, "192.168.3.1", 3.0, [])
        finish, finish_clients = subnet(registry, "192.168.4.1", 1.0, [2.0])
        peer(start, higher_ip)
        peer(higher_ip, finish)
        peer(start, lower_ip)
        peer(lower_ip, finish)
        service = RoutingService(registry)

        service.build()

        assert lower_ip.address.value < higher_ip.address.value
        assert service.get_for(start.address).next_hop(finish_clients[0].address) == lower_ip.address


class TestRoutingServiceGetFor:
    """10 points: get_for enforces build state and performs lookup."""

    def test_get_for_returns_the_precomputed_table_after_build(self) -> None:
        registry = DeviceRegistry()
        router, clients = subnet(registry, "192.168.1.1", 1.0, [2.0])
        service = RoutingService(registry)
        service.build()

        assert service.get_for(clients[0].address).next_hop(router.address) == router.address

    def test_get_for_raises_runtime_error_before_build(self) -> None:
        registry = DeviceRegistry()
        router, _ = subnet(registry, "192.168.1.1", 1.0, [])

        with pytest.raises(RuntimeError) as error:
            RoutingService(registry).get_for(router.address)
        assert type(error.value) is RuntimeError

    def test_get_for_rejects_an_unknown_address_after_build(self) -> None:
        registry = DeviceRegistry()
        subnet(registry, "192.168.1.1", 1.0, [])
        service = RoutingService(registry)
        service.build()

        with pytest.raises(ValueError):
            service.get_for(ip("192.168.1.99"))
