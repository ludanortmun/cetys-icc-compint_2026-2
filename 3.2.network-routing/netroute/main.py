import click

from netroute.address import IPAddress
from netroute.network import Network, Packet

SOURCE = IPAddress.from_string("192.168.1.2")
DEFAULT_MAX_HOPS = 64
DEFAULT_TIMEOUT_SECONDS = 10.0


@click.group()
def main():
    pass


@main.command()
@click.argument("destination")
@click.argument("message")
@click.option("--max-hops", default=DEFAULT_MAX_HOPS, show_default=True,
              help="Maximum number of hops before the packet is dropped.")
@click.option("--timeout", default=DEFAULT_TIMEOUT_SECONDS, show_default=True,
              help="Maximum latency, in seconds, before the packet is dropped.")
def send(destination: str, message: str, max_hops: int, timeout: float):
    network = Network(registry=None)  # Replace with actual DeviceRegistry instance
    dest = IPAddress.from_string(destination)
    packet = Packet(content=message, source=SOURCE, destination_address=dest, ttl=max_hops)
    click.echo(network.send(SOURCE, dest, packet, timeout_ms=timeout * 1000))


@main.command()
@click.argument("destination")
@click.option("--max-hops", default=DEFAULT_MAX_HOPS, show_default=True,
              help="Maximum number of hops before the trace is stopped.")
@click.option("--timeout", default=DEFAULT_TIMEOUT_SECONDS, show_default=True,
              help="Maximum latency, in seconds, before the trace is stopped.")
def trace(destination: str, max_hops: int, timeout: float):
    network = Network(registry=None)  # Replace with actual DeviceRegistry instance
    dest = IPAddress.from_string(destination)
    click.echo(network.trace(SOURCE, dest, max_hops=max_hops, timeout_ms=timeout * 1000))


if __name__ == "__main__":
    main()
