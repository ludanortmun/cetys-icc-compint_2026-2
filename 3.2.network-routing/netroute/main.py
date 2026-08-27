from functools import cache
from time import sleep

import click

from netroute.address import IPAddress
from netroute.factory import create_random_net
from netroute.network import Packet

SOURCE = IPAddress.from_string("192.168.1.2")
DEFAULT_SUBNETS = 10
DEFAULT_MAX_HOPS = 64
DEFAULT_TIMEOUT_SECONDS = 10.0


@cache
def get_network():
    """Return the (lazily created, cached) simulated network."""
    return create_random_net(DEFAULT_SUBNETS)


@click.group()
def main():
    """CLI entry point for sending and tracing packets across the simulated network."""
    pass


@main.command()
@click.argument("destination")
@click.argument("message")
@click.option("--max-hops", default=DEFAULT_MAX_HOPS, show_default=True,
              help="Maximum number of hops before the packet is dropped.")
@click.option("--timeout", default=DEFAULT_TIMEOUT_SECONDS, show_default=True,
              help="Maximum latency, in seconds, before the packet is dropped.")
def send(destination: str, message: str, max_hops: int, timeout: float):
    network = get_network()
    dest = IPAddress.from_string(destination)
    packet = Packet(content=message, source=SOURCE, destination_address=dest, ttl=max_hops)
    result = network.send(SOURCE, dest, packet, timeout_ms=timeout * 1000)
    click.echo(f"{destination}: {message}")
    sleep(result.latency_ms / 1000)
    if result.dropped:
        click.echo(f"Packet dropped after {result.latency_ms:.2f} ms")
    else:
        click.echo(f"Packet delivered in {result.latency_ms:.2f} ms")


@main.command()
@click.argument("destination")
@click.option("--max-hops", default=DEFAULT_MAX_HOPS, show_default=True,
              help="Maximum number of hops before the trace is stopped.")
@click.option("--timeout", default=DEFAULT_TIMEOUT_SECONDS, show_default=True,
              help="Maximum latency, in seconds, before the trace is stopped.")
def trace(destination: str, max_hops: int, timeout: float):
    network = get_network()
    dest = IPAddress.from_string(destination)
    result = network.trace(SOURCE, dest, max_hops, timeout_ms=timeout * 1000)
    for hop, latency in result:
        sleep(latency / 1000)
        click.echo(f"{hop} ({latency:.2f} ms)")
    click.echo()
    if result and result[-1][0] == dest:
        click.echo(f"Trace complete in {sum(latency for _, latency in result):.2f} ms and {len(result)} hops")
    else:
        click.echo(f"Trace stopped after {sum(latency for _, latency in result):.2f} ms and {len(result)} hops")


if __name__ == "__main__":
    main()
