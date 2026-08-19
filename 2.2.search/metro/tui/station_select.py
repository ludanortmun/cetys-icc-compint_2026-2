"""Shared station-selection UX for every metro TUI flow.

Every prompt that asks a user to pick a station should look and behave the
same way: the available stations are listed with a number next to each one,
and the user may respond either with that number or with the station's ID
(case-insensitively).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from metro.station import Station


InputFunction = Callable[[str], str]
OutputFunction = Callable[[str], None]


def station_label(station: Station) -> str:
    """Return the standard ``id (name)`` label used across the TUI."""
    return f"{station.id} ({station.name})"


def select_station(
    stations: Sequence[Station],
    *,
    prompt: str,
    input_fn: InputFunction,
    output_fn: OutputFunction,
    header: str = "Available stations:",
    empty_message: str = "No stations are available.",
    cancel_token: str | None = "B",
    invalid_message: str | None = None,
) -> Station | None:
    """Prompt for a station from ``stations``, numbering them for selection.

    Users may answer with the listed number or with the station ID, matched
    case-insensitively. Returns ``None`` if there are no stations to choose
    from, or if the user enters ``cancel_token`` (when one is provided).
    """
    if not stations:
        output_fn(empty_message)
        return None

    output_fn(header)
    for index, station in enumerate(stations, start=1):
        output_fn(f"  [{index}] {station_label(station)}")
    output_fn("")

    message = invalid_message or (
        "Select a listed number or station ID"
        + (f" (or {cancel_token} to cancel)." if cancel_token else ".")
    )

    while True:
        selection = input_fn(prompt).strip()
        if cancel_token is not None and selection.casefold() == cancel_token.casefold():
            return None

        station = _match_station(selection, stations)
        if station is not None:
            return station

        output_fn(message)


def _match_station(selection: str, stations: Sequence[Station]) -> Station | None:
    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(stations):
            return stations[index]

    normalized = selection.casefold()
    for station in stations:
        if station.id.casefold() == normalized:
            return station
    return None


__all__ = ["select_station", "station_label"]
