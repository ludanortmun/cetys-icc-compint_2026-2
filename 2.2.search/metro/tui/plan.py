"""Interactive trip-planning helpers for the metro terminal UI."""

from __future__ import annotations

from collections.abc import Callable

from metro.network import MetroNetwork
from metro.station import Station, StationRegistry
from metro.topology import ALL_STATIONS
from metro.tui.screen import clear_console


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


def plan_trip(
    network: MetroNetwork,
    *,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
    station_registry: StationRegistry | None = None,
) -> list[Station] | None:
    """Prompt for a trip and display its route.

    Station IDs and station names are accepted case-insensitively.  ``input_fn``
    and ``output_fn`` make this interaction usable both from ``main.py`` and
    from automated tests.
    """
    stations = (
        StationRegistry.from_stations(ALL_STATIONS)
        if station_registry is None
        else station_registry
    )
    if not stations.all_stations():
        clear_console()
        output_fn("No stations are available to plan a trip.")
        return None

    origin_id, destination_id, search_type = prompt_for_trip(
        stations, input_fn, output_fn
    )

    try:
        route = network.find_route(origin_id, destination_id, search_type)
    except Exception as error:
        clear_console()
        output_fn(f"Unable to plan trip: {error}")
        return None

    if not route:
        clear_console()
        output_fn(
            "No route is available from "
            f"{_station_label(origin_id, stations)} to "
            f"{_station_label(destination_id, stations)}."
        )
        return None

    clear_console()
    _display_plan(route, search_type, output_fn)
    return route


def prompt_for_trip(
    station_registry: StationRegistry,
    input_fn: InputFunction = input,
    output_fn: OutputFunction = print,
) -> tuple[str, str, str]:
    """Use the shared planner prompts to select a trip and search algorithm."""
    clear_console()
    _show_available_stations(station_registry, output_fn)
    output_fn("")
    origin_id = _prompt_for_station("Origin", station_registry, input_fn, output_fn)
    destination_id = _prompt_for_station(
        "Destination", station_registry, input_fn, output_fn
    )
    search_type = _prompt_for_search_type(input_fn, output_fn)
    return origin_id, destination_id, search_type


def _show_available_stations(
    station_registry: StationRegistry, output_fn: OutputFunction
) -> None:
    output_fn("Available stations:")
    for station in station_registry.all_stations():
        output_fn(f"  {station.id}: {station.name}")


def _prompt_for_station(
    label: str,
    station_registry: StationRegistry,
    input_fn: InputFunction,
    output_fn: OutputFunction,
) -> str:
    while True:
        selection = input_fn(f"{label} station ID or name: ").strip()
        station_id, matches = _station_matches(selection, station_registry)

        if station_id is not None:
            return station_id
        if matches:
            choices = ", ".join(matches)
            output_fn(
                f'"{selection}" matches more than one station. '
                f"Use a station ID: {choices}."
            )
        else:
            output_fn(
                f'"{selection}" is not a known station ID or name. '
                "Please try again."
            )


def _station_matches(
    selection: str, station_registry: StationRegistry
) -> tuple[str | None, list[str]]:
    """Return an exact ID/name match, or all IDs for an ambiguous name."""
    normalized = _normalize(selection)
    station_ids_by_normalized_id = {
        _normalize(station.id): station.id
        for station in station_registry.all_stations()
    }
    if normalized in station_ids_by_normalized_id:
        return station_ids_by_normalized_id[normalized], []

    matches = [
        station.id
        for station in station_registry.all_stations()
        if _normalize(station.name) == normalized
    ]
    if len(matches) == 1:
        return matches[0], []
    return None, matches


def _prompt_for_search_type(
    input_fn: InputFunction, output_fn: OutputFunction
) -> str:
    choices = {
        "": "bfs",
        "1": "bfs",
        "bfs": "bfs",
        "breadth first": "bfs",
        "breadth-first": "bfs",
        "2": "dfs",
        "dfs": "dfs",
        "depth first": "dfs",
        "depth-first": "dfs",
    }
    while True:
        selection = _normalize(
            input_fn("Search method [1] BFS (default) or [2] DFS: ")
        )
        if selection in choices:
            return choices[selection]
        output_fn("Choose BFS or DFS (or enter 1 or 2).")


def _display_plan(
    route: list[Station], search_type: str, output_fn: OutputFunction
) -> None:
    route_text = " → ".join(
        f"{station.name} ({station.id})" for station in route
    )
    output_fn("=== Trip Plan ===")
    output_fn(f"Route: {route_text}")
    output_fn(f"Stops: {len(route) - 1}")
    output_fn(f"Search: {search_type.upper()}")


def _station_label(station_id: str, station_registry: StationRegistry) -> str:
    station = station_registry.get_station(station_id)
    return f"{station.name} ({station_id})"


def _normalize(value: str) -> str:
    return " ".join(value.split()).casefold()
