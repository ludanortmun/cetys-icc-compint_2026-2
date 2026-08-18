"""Interactive, rider-directed metro navigation."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from textwrap import wrap

from metro.network import MetroNetwork
from metro.station import Station, StationRegistry
from metro.topology import LINE_REGISTRY, ALL_STATIONS


@dataclass(frozen=True)
class RideSummary:
    """The route actually ridden and its derived line information."""

    origin: Station
    destination: Station
    desired_destination: Station | None
    route: tuple[Station, ...]
    leg_lines: tuple[str | None, ...]
    transfers: int

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
    line_registry: Mapping[str, Sequence[str]] | None = None,
) -> RideSummary:
    """Prompt for a ride, navigate it one station at a time, and show its summary.

    ``B`` rides back to the immediately preceding station and records that
    return trip.  ``Q`` ends the ride at the current station.  The optional
    destination is a rider's goal only; the summary always reports the station
    where the ride actually ended.
    """
    stations = (
        StationRegistry.from_stations(ALL_STATIONS)
        if station_registry is None
        else station_registry
    )
    lines = LINE_REGISTRY if line_registry is None else line_registry
    origin = _prompt_station(
        "Origin station ID: ", "origin", stations, input_fn, output_fn
    )
    desired_destination = _prompt_optional_station(
        "Desired destination ID (optional): ",
        stations,
        input_fn,
        output_fn,
    )

    route = [origin]
    while True:
        current_station = route[-1]
        connections = _unique_connections(
            network.get_connected_stations(current_station.id)
        )
        output_fn(
            render_metro_ride(
                origin=origin,
                desired_destination=desired_destination,
                route=route,
                connections=connections,
            )
        )
        choice = input_fn("Choose a station, [B]ack, or [Q]uit: ").strip()
        command = choice.casefold()

        if command == "q":
            break
        if command == "b":
            _go_back(route, connections, output_fn)
            continue

        next_station = _select_connection(choice, connections)
        if next_station is None:
            output_fn("Choose a listed station number or station ID.")
            continue
        route.append(next_station)

    summary = build_ride_summary(route, desired_destination, lines)
    output_fn(render_trip_summary(summary))
    return summary


def build_ride_summary(
    route: Sequence[Station],
    desired_destination: Station | None = None,
    line_registry: Mapping[str, Sequence[str]] | None = None,
) -> RideSummary:
    """Build a summary for an already-ridden route.

    This is separate from the terminal interaction so callers such as
    ``main.py`` can present or persist a ride however they need.
    """
    if not route:
        raise ValueError("A ride must contain an origin station.")

    lines = LINE_REGISTRY if line_registry is None else line_registry
    ridden_route = tuple(route)
    leg_lines = derive_route_lines(ridden_route, lines)
    return RideSummary(
        origin=ridden_route[0],
        destination=ridden_route[-1],
        desired_destination=desired_destination,
        route=ridden_route,
        leg_lines=leg_lines,
        transfers=_count_transfers(leg_lines),
    )


def derive_route_lines(
    route: Sequence[Station],
    line_registry: Mapping[str, Sequence[str]] | None = None,
) -> tuple[str | None, ...]:
    """Return one selected line for each consecutive pair in ``route``.

    A segment may occur on more than one line.  In that case, line assignments
    are chosen across the whole route to minimize changes, rather than assuming
    the first matching line is always the one the rider used.  Segments absent
    from the registry are marked ``None`` instead of causing the ride summary
    to fail.
    """
    lines = LINE_REGISTRY if line_registry is None else line_registry
    possible_lines = [
        _lines_for_station_pair(from_station.id, to_station.id, lines)
        for from_station, to_station in zip(route, route[1:])
    ]
    if not possible_lines:
        return ()

    # Dynamic programming preserves registry order as a deterministic tie
    # breaker while choosing assignments with the fewest line changes.
    line_order = {line_name: index for index, line_name in enumerate(lines)}
    states: dict[str | None, tuple[int, tuple[int, ...], tuple[str | None, ...]]] = {}
    for line_name in possible_lines[0] or (None,):
        states[line_name] = (0, (line_order.get(line_name, -1),), (line_name,))

    for candidates in possible_lines[1:]:
        next_states: dict[
            str | None, tuple[int, tuple[int, ...], tuple[str | None, ...]]
        ] = {}
        for next_line in candidates or (None,):
            next_order = line_order.get(next_line, -1)
            for previous_line, (cost, order, assignment) in states.items():
                transfer = (
                    previous_line is not None
                    and next_line is not None
                    and previous_line != next_line
                )
                candidate = (
                    cost + int(transfer),
                    order + (next_order,),
                    assignment + (next_line,),
                )
                existing = next_states.get(next_line)
                if existing is None or candidate[:2] < existing[:2]:
                    next_states[next_line] = candidate
        states = next_states

    return min(states.values(), key=lambda state: state[:2])[2]


def render_metro_ride(
    *,
    origin: Station,
    desired_destination: Station | None,
    route: Sequence[Station],
    connections: Sequence[Station],
) -> str:
    """Render the current station and its available rider-directed choices."""
    lines = [
        f"Origin: {_station_label(origin)}",
        (
            f"Desired destination: {_station_label(desired_destination)}"
            if desired_destination is not None
            else "Desired destination: Not specified"
        ),
        f"Current station: {_station_label(route[-1])}",
        f"Route so far: {_format_route(route)}",
        "Next stations:",
    ]
    lines.extend(
        f"  [{index}] {_station_label(station)}"
        for index, station in enumerate(connections, start=1)
    )
    if not connections:
        lines.append("  No connected stations are currently available.")
    lines.extend(("[B] Go back", "[Q] End ride"))
    return _render_box("METRO RIDE", lines)


def render_trip_summary(summary: RideSummary) -> str:
    """Render the final summary using the route that was actually ridden."""
    desired_line: list[str] = []
    if (
        summary.desired_destination is not None
        and summary.desired_destination.id != summary.destination.id
    ):
        desired_line.append(
            f"Desired destination: {_station_label(summary.desired_destination)} (not reached)"
        )

    return _render_box(
        "TRIP SUMMARY",
        [
            f"Origin: {_station_label(summary.origin)}",
            f"Destination: {_station_label(summary.destination)}",
            *desired_line,
            f"Stations: {summary.stations_visited}",
            f"Transfers: {summary.transfers}",
            f"Full route: {_format_route(summary.route)}",
        ],
    )


def _prompt_station(
    prompt: str,
    station_role: str,
    station_registry: StationRegistry,
    input_fn: InputFunction,
    output_fn: OutputFunction,
) -> Station:
    if not station_registry.all_stations():
        raise ValueError("Cannot start a ride without registered stations.")

    output_fn(_station_directory(station_registry))
    while True:
        station = _station_for_id(input_fn(prompt), station_registry)
        if station is not None:
            return station
        output_fn(f"Unknown {station_role} station. Enter one of the listed station IDs.")


def _prompt_optional_station(
    prompt: str,
    station_registry: StationRegistry,
    input_fn: InputFunction,
    output_fn: OutputFunction,
) -> Station | None:
    while True:
        station_id = input_fn(prompt).strip()
        if not station_id:
            return None
        station = _station_for_id(station_id, station_registry)
        if station is not None:
            return station
        output_fn("Unknown destination station. Press Enter to leave it unspecified.")


def _station_for_id(
    station_id: str,     station_registry: StationRegistry
) -> Station | None:
    normalized_id = station_id.strip().casefold()
    for station in station_registry.all_stations():
        if station.id.casefold() == normalized_id:
            return station
    return None


def _station_directory(station_registry: StationRegistry) -> str:
    entries = ", ".join(
        _station_label(station) for station in station_registry.all_stations()
    )
    return f"Available stations: {entries}"


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
    choice: str, connections: Sequence[Station]
) -> Station | None:
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(connections):
            return connections[index]

    normalized_id = choice.casefold()
    for station in connections:
        if station.id.casefold() == normalized_id:
            return station
    return None


def _go_back(
    route: list[Station], connections: Sequence[Station], output_fn: OutputFunction
) -> None:
    if len(route) == 1:
        output_fn("Already at the origin station.")
        return

    previous_station = route[-2]
    if any(station.id == previous_station.id for station in connections):
        route.append(previous_station)
        return
    output_fn("The previous station is not currently connected.")


def _lines_for_station_pair(
    from_station_id: str,
    to_station_id: str,
    line_registry: Mapping[str, Sequence[str]],
) -> tuple[str, ...]:
    matching_lines: list[str] = []
    for line_name, station_ids in line_registry.items():
        try:
            adjacent_pairs = zip(station_ids, station_ids[1:])
        except (TypeError, KeyError):
            continue
        if any(
            (left == from_station_id and right == to_station_id)
            or (left == to_station_id and right == from_station_id)
            for left, right in adjacent_pairs
        ):
            matching_lines.append(line_name)
    return tuple(matching_lines)


def _count_transfers(leg_lines: Sequence[str | None]) -> int:
    return sum(
        previous_line is not None
        and next_line is not None
        and previous_line != next_line
        for previous_line, next_line in zip(leg_lines, leg_lines[1:])
    )


def _station_label(station: Station) -> str:
    return f"{station.name} ({station.id})"


def _format_route(route: Sequence[Station]) -> str:
    return " -> ".join(_station_label(station) for station in route)


def _render_box(title: str, lines: Sequence[str], width: int = 72) -> str:
    inner_width = max(width - 4, len(title) + 2)
    border = "+" + "-" * (inner_width + 2) + "+"
    rendered = [border, f"| {title.center(inner_width)} |", border]
    for line in lines:
        for wrapped_line in wrap(line, width=inner_width) or [""]:
            rendered.append(f"| {wrapped_line.ljust(inner_width)} |")
    rendered.append(border)
    return "\n".join(rendered)