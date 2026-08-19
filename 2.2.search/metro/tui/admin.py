"""Terminal UI flows for temporarily administering metro segments."""

from __future__ import annotations

from collections.abc import Callable

from metro.network import MetroNetwork
from metro.station import Station, StationRegistry
from metro.topology import ALL_STATIONS
from metro.tui.screen import clear_console
from metro.tui.station_select import select_station, station_label


Input = Callable[[str], str]
Output = Callable[[str], None]


def administer_network(
    network: MetroNetwork,
    input_fn: Input = input,
    output_fn: Output = print,
) -> None:
    """Run the segment-administration menu until the operator goes back."""
    while True:
        clear_console()
        output_fn("\nMetro administration")
        output_fn("1. Close a segment")
        output_fn("2. View/reopen closed segments")
        output_fn("3. Back")
        output_fn("")

        choice = input_fn("Select an option: ").strip()
        if choice == "1":
            close_segment_flow(network, input_fn, output_fn)
        elif choice == "2":
            reopen_segment_flow(network, input_fn, output_fn)
        elif choice == "3":
            return
        else:
            output_fn("Invalid option. Select 1, 2, or 3.")


def close_segment_flow(
    network: MetroNetwork,
    input_fn: Input = input,
    output_fn: Output = print,
) -> None:
    """Select an open directed segment to close."""
    station_registry = StationRegistry.from_stations(ALL_STATIONS)
    from_station = _select_station(station_registry, input_fn, output_fn)
    if from_station is None:
        return

    clear_console()
    connections = network.get_connected_stations(from_station.id)
    to_station = _select_connection(
        from_station, connections, input_fn, output_fn
    )
    if to_station is None:
        return

    clear_console()
    try:
        network.close_segment(from_station.id, to_station.id)
    except ValueError as error:
        output_fn(
            f"Could not close {from_station.id} -> {to_station.id}: {error}"
        )
    else:
        output_fn(f"Closed segment: {from_station.id} -> {to_station.id}.")
    _wait_for_service_operations(input_fn)


def reopen_segment_flow(
    network: MetroNetwork,
    input_fn: Input = input,
    output_fn: Output = print,
) -> None:
    """List closed segments and optionally reopen a selected one."""
    clear_console()
    closed_segments = _show_closed_segments(network, output_fn)
    if not closed_segments:
        _wait_for_service_operations(input_fn)
        return

    selection = input_fn("Select a segment to reopen (or B to go back): ").strip()
    if selection.casefold() == "b":
        return

    try:
        segment_index = int(selection) - 1
    except ValueError:
        output_fn("Invalid segment selection.")
        _wait_for_service_operations(input_fn)
        return

    if segment_index not in range(len(closed_segments)):
        output_fn("Invalid segment selection.")
        _wait_for_service_operations(input_fn)
        return

    from_station, to_station = closed_segments[segment_index]
    try:
        network.open_segment(from_station.id, to_station.id)
    except ValueError as error:
        output_fn(
            f"Could not reopen {from_station.id} -> {to_station.id}: {error}"
        )
    else:
        output_fn(
            f"Reopened segment: {from_station.id} -> {to_station.id}."
        )
    _wait_for_service_operations(input_fn)


def _show_closed_segments(
    network: MetroNetwork, output_fn: Output = print
) -> list[tuple[Station, Station]]:
    """Display closed segments and return them in their selectable order."""
    clear_console()
    try:
        closed_segments = network.get_closed_segments()
    except ValueError as error:
        output_fn(f"Could not retrieve closed segments: {error}")
        return []

    if not closed_segments:
        output_fn("No segments are currently closed; all services are operational.")
        return []

    output_fn("Closed segments:")
    for index, (from_station, to_station) in enumerate(closed_segments, start=1):
        output_fn(
            f"{index}. {station_label(from_station)} -> "
            f"{station_label(to_station)}"
        )
    return closed_segments


def _select_station(
    station_registry: StationRegistry,
    input_fn: Input,
    output_fn: Output,
) -> Station | None:
    """Select the source station from every registered station."""
    station = select_station(
        station_registry.all_stations(),
        prompt="Select a station (number, ID, or B to cancel): ",
        input_fn=input_fn,
        output_fn=output_fn,
        header="Select the station to close from:",
        empty_message="No stations are configured.",
    )
    if station is None:
        output_fn("Segment closure cancelled.")
    return station


def _select_connection(
    from_station: Station,
    connections: list[Station],
    input_fn: Input,
    output_fn: Output,
) -> Station | None:
    """Select the destination from segments currently open from ``from_station``."""
    station = select_station(
        connections,
        prompt="Select a destination (number, ID, or B to cancel): ",
        input_fn=input_fn,
        output_fn=output_fn,
        header=f"Select an open segment from {station_label(from_station)}:",
        empty_message=f"No open segments leave {station_label(from_station)}.",
    )
    if station is None and connections:
        output_fn("Segment closure cancelled.")
    return station


def _wait_for_service_operations(input_fn: Input) -> None:
    """Keep an operation result visible before the admin menu is redrawn."""
    input_fn("Press Enter to return to service operations...")


__all__ = [
    "administer_network",
    "close_segment_flow",
    "reopen_segment_flow",
]
