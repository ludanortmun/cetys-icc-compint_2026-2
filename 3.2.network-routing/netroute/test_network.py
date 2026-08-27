"""Checklist-style grading tests for Network.send and Network.trace (50 points)."""

import pytest

from netroute.address import IPAddress
from netroute.factory import (
    create_fiber_router,
    create_subnet,
    create_wired_client,
)
from netroute.network import Network, Packet, TransmissionResult
from netroute.registry import DeviceRegistry
from netroute.routing_service import RoutingService


def ip(value: str) -> IPAddress:
    return IPAddress.from_string(value)


def build_network():
    """Build deterministic A-B-C plus disconnected D subnets."""
    registry = DeviceRegistry()

    def add(router: str, router_latency: float, clients: list[float]):
        return create_subnet(
            registry,
            ip(router),
            len(clients),
            create_fiber_router,
            create_wired_client,
            router_latency,
            clients,
        )

    router_a, clients_a = add("192.168.1.1", 1.0, [2.0, 4.0])
    router_b, clients_b = add("192.168.2.1", 3.0, [6.0])
    router_c, clients_c = add("192.168.3.1", 5.0, [7.0])
    router_d, clients_d = add("192.168.4.1", 11.0, [13.0])
    router_a.with_peers([router_b.address])
    router_b.with_peers([router_a.address, router_c.address])
    router_c.with_peers([router_b.address])
    service = RoutingService(registry)
    service.build()
    network = Network(registry, service)
    return network, (router_a, router_b, router_c, router_d), (
        clients_a,
        clients_b,
        clients_c,
        clients_d,
    )


def packet(source: IPAddress, dest: IPAddress, ttl: int = 64) -> Packet:
    return Packet("grading", source, dest, ttl)


class TestNetworkSend:
    """25 points: send delivers, accounts for budgets, and drops safely."""

    def test_send_delivers_across_subnets_with_accumulated_latency(self) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        assert network.send(source.address, dest.address, packet(source.address, dest.address)) == (
            TransmissionResult(27.0, False)
        )

    def test_send_delivers_between_clients_in_the_same_subnet(self) -> None:
        network, _, clients = build_network()
        source, dest = clients[0]

        assert network.send(source.address, dest.address, packet(source.address, dest.address)) == (
            TransmissionResult(8.0, False)
        )

    @pytest.mark.parametrize("ttl,dropped", [(4, False), (3, True)])
    def test_send_allows_exact_ttl_and_drops_when_exceeded(
        self, ttl: int, dropped: bool
    ) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        result = network.send(
            source.address, dest.address, packet(source.address, dest.address, ttl)
        )

        assert result.dropped is dropped

    @pytest.mark.parametrize("timeout,dropped", [(27.0, False), (26.999, True)])
    def test_send_allows_exact_timeout_and_drops_when_exceeded(
        self, timeout: float, dropped: bool
    ) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        result = network.send(
            source.address,
            dest.address,
            packet(source.address, dest.address),
            timeout_ms=timeout,
        )

        assert result.dropped is dropped

    @pytest.mark.parametrize(
        ("source", "dest"),
        [
            ("192.168.9.9", "192.168.3.2"),
            ("192.168.1.2", "192.168.9.9"),
        ],
        ids=["unknown-source", "unknown-destination"],
    )
    def test_send_drops_unknown_endpoints(self, source: str, dest: str) -> None:
        network, _, _ = build_network()

        assert network.send(ip(source), ip(dest), packet(ip(source), ip(dest))) == (
            TransmissionResult(0.0, True)
        )

    def test_send_drops_an_unreachable_disconnected_destination(self) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[3][0]

        assert network.send(source.address, dest.address, packet(source.address, dest.address)) == (
            TransmissionResult(3.0, True)
        )

    def test_send_drops_a_missing_host_in_a_known_reachable_subnet(self) -> None:
        network, _, clients = build_network()
        source = clients[0][0]
        missing = ip("192.168.3.99")
        assert network.send(source.address, missing, packet(source.address, missing)) == (
            TransmissionResult(15.0, True)
        )


class TestNetworkTrace:
    """25 points: trace reports reached hops, link costs, and boundaries."""

    def test_trace_starts_at_source_and_reports_each_link_latency(self) -> None:
        network, routers, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        assert network.trace(source.address, dest.address) == [
            (source.address, 0.0),
            (routers[0].address, 3.0),
            (routers[1].address, 4.0),
            (routers[2].address, 8.0),
            (dest.address, 12.0),
        ]

    @pytest.mark.parametrize(
        ("max_hops", "expected_length", "reaches_dest"),
        [(4, 5, True), (3, 4, False)],
    )
    def test_trace_allows_exact_max_hops_and_stops_when_exceeded(
        self, max_hops: int, expected_length: int, reaches_dest: bool
    ) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        trace = network.trace(source.address, dest.address, max_hops=max_hops)

        assert len(trace) == expected_length
        assert (trace[-1][0] == dest.address) is reaches_dest

    @pytest.mark.parametrize(
        ("timeout", "expected_length", "reaches_dest"),
        [(27.0, 5, True), (26.999, 4, False)],
    )
    def test_trace_allows_exact_timeout_and_stops_before_exceeding_it(
        self, timeout: float, expected_length: int, reaches_dest: bool
    ) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        trace = network.trace(source.address, dest.address, timeout_ms=timeout)

        assert len(trace) == expected_length
        assert (trace[-1][0] == dest.address) is reaches_dest

    @pytest.mark.parametrize(
        ("source", "dest"),
        [
            ("192.168.9.9", "192.168.3.2"),
            ("192.168.1.2", "192.168.9.9"),
        ],
        ids=["unknown-source", "unknown-destination"],
    )
    def test_trace_returns_empty_for_unknown_endpoints(
        self, source: str, dest: str
    ) -> None:
        network, _, _ = build_network()

        assert network.trace(ip(source), ip(dest)) == []

    def test_trace_returns_partial_path_for_a_disconnected_destination(self) -> None:
        network, routers, clients = build_network()
        source, dest = clients[0][0], clients[3][0]

        assert network.trace(source.address, dest.address) == [
            (source.address, 0.0),
            (routers[0].address, 3.0),
        ]

    def test_trace_returns_partial_path_for_missing_host_in_known_subnet(self) -> None:
        network, routers, clients = build_network()
        source = clients[0][0]
        missing = ip("192.168.3.99")

        assert network.trace(source.address, missing) == [
            (source.address, 0.0),
            (routers[0].address, 3.0),
            (routers[1].address, 4.0),
            (routers[2].address, 8.0),
        ]

    def test_successful_trace_latency_equals_send_latency(self) -> None:
        network, _, clients = build_network()
        source, dest = clients[0][0], clients[2][0]

        trace = network.trace(source.address, dest.address)
        sent = network.send(
            source.address, dest.address, packet(source.address, dest.address)
        )

        assert trace[-1][0] == dest.address
        assert sum(latency for _, latency in trace) == sent.latency_ms
