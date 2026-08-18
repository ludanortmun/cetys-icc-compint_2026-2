"""Main menu for the interactive metro terminal application."""

from __future__ import annotations

from collections.abc import Callable

from metro.network import MetroNetwork
from metro.station import StationRegistry
from metro.topology import ALL_STATIONS, LINE_REGISTRY
from metro.tui.admin import administer_network
from metro.tui.assistant import run_trip_assistant
from metro.tui.healthcheck import render_healthcheck
from metro.tui.map import show_map
from metro.tui.navigate import ride_metro
from metro.tui.plan import plan_trip


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], object]


def init_network() -> MetroNetwork:
    """Build the production network from the configured line registry."""
    network = MetroNetwork(StationRegistry.from_stations(ALL_STATIONS))
    for line_id, station_ids in LINE_REGISTRY.items():
        network.add_line(line_id, station_ids)
    return network


def main_loop(
    network: MetroNetwork | None = None,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> None:
    """Run the metro menu until the rider chooses to exit.

    ``network`` and the I/O callables are optional to preserve the original
    no-argument entry point while making the menu straightforward to embed and
    test.
    """
    if network is None:
        network = init_network()

    while True:
        output_fn(render_healthcheck(network))
        output_fn("Welcome to the Metro System!")
        output_fn("1. View map")
        output_fn("2. Plan trip")
        output_fn("3. Ride metro")
        output_fn("4. Service operations/admin")
        output_fn("5. Trip Assistant")
        output_fn("0. Exit")

        choice = input_fn("Enter your choice: ").strip()
        if choice == "1":
            show_map(output=output_fn)
        elif choice == "2":
            plan_trip(network, input_fn=input_fn, output_fn=output_fn)
        elif choice == "3":
            ride_metro(network, input_fn=input_fn, output_fn=output_fn)
        elif choice == "4":
            administer_network(network, input_fn=input_fn, output_fn=output_fn)
        elif choice == "5":
            run_trip_assistant(network, input_fn=input_fn, output_fn=output_fn)
        elif choice == "0":
            output_fn("Goodbye.")
            return
        else:
            output_fn("Invalid option. Select 0 through 5.")


if __name__ == "__main__":
    main_loop()
