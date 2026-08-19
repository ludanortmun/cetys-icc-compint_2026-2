"""Interactive, rider-directed metro navigation."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from textwrap import wrap

from metro.network import MetroNetwork
from metro.station import Station, StationRegistry
from metro.topology import ALL_STATIONS
from metro.tui.screen import clear_console
from metro.tui.station_select import select_station, station_label


@dataclass(frozen=True)
class RideSummary:
    """The route actually ridden and its derived line information."""

    origin: Station
    destination: Station
    route: tuple[Station, ...]

    @property
    def stations_visited(self) -> int:
        """Return the number of route entries, including the origin."""
        return len(self.route)


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


def ride_metro(
    network: MetroNetwork,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
    *,
    station_registry: StationRegistry | None = None,
) -> RideSummary:
    """Prompt for a ride, navigate it one station at a time, and show its summary.

    ``B`` rides back to the immediately preceding station and records that
    return trip. ``Q`` ends the ride at the current station.
    """
    stations = (
        StationRegistry.from_stations(ALL_STATIONS)
        if station_registry is None
        else station_registry
    )
    origin = _prompt_station(
        "Origin station (number or ID): ", stations, input_fn, output_fn
    )

    route = [origin]
    while True:
        current_station = route[-1]
        connections = _unique_connections(
            network.get_connected_stations(current_station.id)
        )
        previous_station = route[-2] if len(route) > 1 else None
        next_stations = [
            (index, station)
            for index, station in enumerate(connections, start=1)
            if station.id != getattr(previous_station, "id", None)
        ]
        can_go_back = (
            previous_station is not None
            and any(
                station.id == previous_station.id for station in connections
            )
        )
        clear_console()
        output_fn(
            render_metro_ride(
                current_station=current_station,
                next_stations=next_stations,
                previous_station=previous_station if can_go_back else None,
            )
        )
        choice = input_fn("Choose a station, [B]ack, or [Q]uit: ").strip()
        command = choice.casefold()

        if command == "q":
            break
        if command == "b":
            _go_back(route, can_go_back, output_fn)
            continue

        next_station = _select_connection(choice, next_stations)
        if next_station is None:
            output_fn("Choose a listed station number or station ID.")
            continue
        route.append(next_station)

    summary = build_ride_summary(route)
    clear_console()
    output_fn(render_trip_summary(summary))
    return summary


def build_ride_summary(
    route: Sequence[Station],
) -> RideSummary:
    """Build a summary for an already-ridden route.

    This is separate from the terminal interaction so callers such as
    ``main.py`` can present or persist a ride however they need.
    """
    if not route:
        raise ValueError("A ride must contain an origin station.")

    ridden_route = tuple(route)
    return RideSummary(
        origin=ridden_route[0],
        destination=ridden_route[-1],
        route=ridden_route,
    )


def render_metro_ride(
    *,
    current_station: Station,
    next_stations: Sequence[tuple[int, Station]],
    previous_station: Station | None,
) -> str:
    """Render the current station and its available rider-directed choices."""
    lines = [
        f"You are currently at {station_label(current_station)}",
        "",
        "Next stations:",
    ]
    lines.extend(
        f"  [{index}] {station_label(station)}"
        for index, station in next_stations
    )
    if not next_stations:
        lines.append("  No further stations to travel to.")
    if previous_station is not None:
        lines.append(f"  [B] Go back to {station_label(previous_station)}")
    lines.extend(("", "[Q] End ride"))
    return _render_box("METRO RIDE", lines)


def render_trip_summary(summary: RideSummary) -> str:
    """Render the final summary using the route that was actually ridden."""
    return _render_box(
        "TRIP SUMMARY",
        [
            f"Origin: {station_label(summary.origin)}",
            f"Destination: {station_label(summary.destination)}",
            f"Stations: {summary.stations_visited}",
            f"Full route: {_format_route(summary.route)}",
        ],
    )


def _prompt_station(
    prompt: str,
    station_registry: StationRegistry,
    input_fn: InputFunction,
    output_fn: OutputFunction,
) -> Station:
    if not station_registry.all_stations():
        raise ValueError("Cannot start a ride without registered stations.")

    return select_station(
        station_registry.all_stations(),
        prompt=prompt,
        input_fn=input_fn,
        output_fn=output_fn,
        cancel_token=None,
    )


def _unique_connections(connections: Sequence[Station]) -> list[Station]:
    seen_station_ids: set[str] = set()
    unique_connections: list[Station] = []
    for station in connections:
        if station.id in seen_station_ids:
            continue
        seen_station_ids.add(station.id)
        unique_connections.append(station)
    return unique_connections


def _select_connection(
    choice: str, connections: Sequence[tuple[int, Station]]
) -> Station | None:
    if choice.isdigit():
        selected_index = int(choice)
        for index, station in connections:
            if index == selected_index:
                return station

    normalized_id = choice.casefold()
    for _, station in connections:
        if station.id.casefold() == normalized_id:
            return station
    return None


def _go_back(route: list[Station], can_go_back: bool, output_fn: OutputFunction) -> None:
    if len(route) == 1:
        output_fn("Already at the origin station.")
        return

    if can_go_back:
        route.append(route[-2])
        return
    output_fn("The previous station is not currently connected.")


def _format_route(route: Sequence[Station]) -> str:
    return " -> ".join(station_label(station) for station in route)


def _render_box(title: str, lines: Sequence[str], width: int = 72) -> str:
    inner_width = max(width - 4, len(title) + 2)
    border = "+" + "-" * (inner_width + 2) + "+"
    rendered = [border, f"| {title.center(inner_width)} |", border]
    for line in lines:
        for wrapped_line in wrap(line, width=inner_width) or [""]:
            rendered.append(f"| {wrapped_line.ljust(inner_width)} |")
    rendered.append(border)
    return "\n".join(rendered)