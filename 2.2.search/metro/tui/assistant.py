"""Interactive, line-aware directions for the extra-credit trip assistant."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Literal

from metro.network import MetroNetwork, RouteSegment
from metro.station import StationRegistry
from metro.topology import ALL_STATIONS
from metro.tui.plan import prompt_for_trip
from metro.tui.screen import clear_console


SearchType = Literal["bfs", "dfs"]
InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], object]


def format_route_directions(segments: Sequence[RouteSegment]) -> list[str]:
    """Return directions after combining adjacent segments on the same line."""
    if not segments:
        return []

    grouped_segments: list[RouteSegment] = []
    for segment in segments:
        if grouped_segments and grouped_segments[-1].line == segment.line:
            grouped_segments[-1] = RouteSegment(
                line=segment.line,
                boarding_station_id=grouped_segments[-1].boarding_station_id,
                exit_station_id=segment.exit_station_id,
            )
        else:
            grouped_segments.append(segment)

    directions = []
    for index, segment in enumerate(grouped_segments):
        prefix = "Take" if index == 0 else "Then take"
        directions.append(
            f"{prefix} Line {segment.line} at {segment.boarding_station_id} "
            f"until {segment.exit_station_id}."
        )
    return directions


def get_trip_directions(
    network: MetroNetwork,
    origin_station_id: str,
    destination_station_id: str,
    search_type: SearchType = "bfs",
) -> list[str]:
    """Find and format a trip, including helpful terminal-route messages."""
    segments = network.find_route_with_lines(
        origin_station_id, destination_station_id, search_type
    )

    if origin_station_id == destination_station_id:
        return [f"You are already at {origin_station_id}."]
    if not segments:
        return [
            f"No route is available from {origin_station_id} "
            f"to {destination_station_id}."
        ]
    return format_route_directions(segments)


def run_trip_assistant(
    network: MetroNetwork,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
    *,
    search_type: SearchType | None = None,
) -> list[str]:
    """Prompt for a trip, print directions, and return them for callers.

    The station and algorithm prompts match the regular trip planner exactly.
    Supplying ``search_type`` keeps the algorithm fixed but still uses the
    shared station-selection screens.
    """
    station_registry = StationRegistry.from_stations(ALL_STATIONS)
    if not station_registry.all_stations():
        clear_console()
        output_fn("No stations are available to plan a trip.")
        return []

    origin_station_id, destination_station_id, selected_search_type = prompt_for_trip(
        station_registry, input_fn, output_fn
    )
    effective_search_type: SearchType = (
        search_type
        if search_type is not None
        else "dfs" if selected_search_type == "dfs" else "bfs"
    )

    try:
        directions = get_trip_directions(
            network,
            origin_station_id,
            destination_station_id,
            effective_search_type,
        )
    except ValueError as error:
        clear_console()
        output_fn(f"Unable to plan trip: {error}")
        return []

    clear_console()
    for direction in directions:
        output_fn(direction)
    return directions
