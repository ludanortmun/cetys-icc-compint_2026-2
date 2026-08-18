"""Terminal UI flows for temporarily administering metro segments."""

from __future__ import annotations

from collections.abc import Callable

from metro.network import MetroNetwork
from metro.station import Station


Input = Callable[[str], str]
Output = Callable[[str], None]


def administer_network(
    network: MetroNetwork,
    input_fn: Input = input,
    output_fn: Output = print,
) -> None:
    """Run the segment-administration menu until the operator goes back."""
    while True:
        output_fn("\nMetro administration")
        output_fn("1. Close a segment")
        output_fn("2. Reopen a segment")
        output_fn("3. View closed segments")
        output_fn("4. Back")

        choice = input_fn("Select an option: ").strip()
        if choice == "1":
            close_segment_flow(network, input_fn, output_fn)
        elif choice == "2":
            reopen_segment_flow(network, input_fn, output_fn)
        elif choice == "3":
            view_closed_segments(network, output_fn)
        elif choice == "4":
            return
        else:
            output_fn("Invalid option. Select 1, 2, 3, or 4.")


def close_segment_flow(
    network: MetroNetwork,
    input_fn: Input = input,
    output_fn: Output = print,
) -> None:
    """Prompt for the directed segment to close and report the result."""
    from_station_id, to_station_id = prompt_directed_segment(input_fn)
    try:
        network.close_segment(from_station_id, to_station_id)
    except ValueError as error:
        output_fn(
            f"Could not close {from_station_id} -> {to_station_id}: {error}"
        )
    else:
        output_fn(f"Closed segment: {from_station_id} -> {to_station_id}.")


def reopen_segment_flow(
    network: MetroNetwork,
    input_fn: Input = input,
    output_fn: Output = print,
) -> None:
    """Let the operator select one displayed closed segment to reopen."""
    closed_segments = view_closed_segments(network, output_fn)
    if not closed_segments:
        return

    selection = input_fn(
        "Select a directed segment to reopen (or B to cancel): "
    ).strip()
    if selection.casefold() == "b":
        output_fn("Reopen cancelled.")
        return

    try:
        segment_index = int(selection) - 1
    except ValueError:
        output_fn("Invalid segment selection.")
        return

    if segment_index not in range(len(closed_segments)):
        output_fn("Invalid segment selection.")
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


def view_closed_segments(
    network: MetroNetwork, output_fn: Output = print
) -> list[tuple[Station, Station]]:
    """Display closed segments and return them in their selectable order."""
    try:
        closed_segments = network.get_closed_segments()
    except ValueError as error:
        output_fn(f"Could not retrieve closed segments: {error}")
        return []

    if not closed_segments:
        output_fn("No segments are currently closed.")
        return []

    output_fn("Closed segments:")
    for index, (from_station, to_station) in enumerate(closed_segments, start=1):
        output_fn(
            f"{index}. {_format_station(from_station)} -> "
            f"{_format_station(to_station)}"
        )
    return closed_segments


def prompt_directed_segment(input_fn: Input = input) -> tuple[str, str]:
    """Collect a directed A-to-B segment, preserving the operator's order."""
    from_station_id = input_fn("Station A ID (from): ").strip()
    to_station_id = input_fn("Station B ID (to): ").strip()
    return from_station_id, to_station_id


def _format_station(station: Station) -> str:
    return f"{station.id} ({station.name})"


__all__ = [
    "administer_network",
    "close_segment_flow",
    "prompt_directed_segment",
    "reopen_segment_flow",
    "view_closed_segments",
]
