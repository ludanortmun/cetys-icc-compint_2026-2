"""Terminal UI flows for temporarily administering metro segments."""

from __future__ import annotations

from collections.abc import Callable

from metro.network import MetroNetwork
from metro.station import Station, StationRegistry
from metro.topology import ALL_STATIONS
from metro.tui.screen import clear_console


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
            f"{index}. {_format_station(from_station)} -> "
            f"{_format_station(to_station)}"
        )
    return closed_segments


def _select_station(
    station_registry: StationRegistry,
    input_fn: Input,
    output_fn: Output,
) -> Station | None:
    """Select the source station from every registered station."""
    stations = station_registry.all_stations()
    if not stations:
        output_fn("No stations are configured.")
        return None

    output_fn("Select the station to close from:")
    for index, station in enumerate(stations, start=1):
        output_fn(f"  [{index}] {_format_station(station)}")
    output_fn("")

    return _select_from_options(
        stations, "Select a station (or B to cancel): ", input_fn, output_fn
    )


def _select_connection(
    from_station: Station,
    connections: list[Station],
    input_fn: Input,
    output_fn: Output,
) -> Station | None:
    """Select the destination from segments currently open from ``from_station``."""
    if not connections:
        output_fn(f"No open segments leave {_format_station(from_station)}.")
        return None

    output_fn(f"Select an open segment from {_format_station(from_station)}:")
    for index, station in enumerate(connections, start=1):
        output_fn(f"  [{index}] {_format_station(station)}")
    output_fn("")

    return _select_from_options(
        connections, "Select a destination (or B to cancel): ", input_fn, output_fn
    )


def _select_from_options(
    options: list[Station],
    prompt: str,
    input_fn: Input,
    output_fn: Output,
) -> Station | None:
    while True:
        selection = input_fn(prompt).strip()
        if selection.casefold() == "b":
            output_fn("Segment closure cancelled.")
            return None
        if selection.isdigit():
            index = int(selection) - 1
            if 0 <= index < len(options):
                return options[index]
        output_fn("Select a listed number or B to cancel.")


def _wait_for_service_operations(input_fn: Input) -> None:
    """Keep an operation result visible before the admin menu is redrawn."""
    input_fn("Press Enter to return to service operations...")


def _format_station(station: Station) -> str:
    return f"{station.id} ({station.name})"


__all__ = [
    "administer_network",
    "close_segment_flow",
    "reopen_segment_flow",
]
