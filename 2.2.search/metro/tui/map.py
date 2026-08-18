"""Text rendering for the metro map."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence

from metro import topology
from metro.station import StationRegistry


def render_map(
    line_registry: Mapping[str, Sequence[str]] | None = None,
    station_registry: StationRegistry | None = None,
) -> list[str]:
    """Return the metro map as display-ready lines.

    Registries are resolved when called so topology changes are reflected without
    re-importing this module.
    """
    lines = topology.LINE_REGISTRY if line_registry is None else line_registry
    stations = (
        StationRegistry.from_stations(topology.ALL_STATIONS)
        if station_registry is None
        else station_registry
    )

    if not lines:
        return ["Metro map:", "No lines configured."]

    station_lines = _station_lines(lines)
    rendered = ["Metro map:"]
    for line_name, station_ids in lines.items():
        stops = [
            _station_label(station_id, stations, station_lines[station_id], line_name)
            for station_id in station_ids
        ]
        rendered.append(
            f"{line_name}: {' -> '.join(stops) if stops else '(no stations)'}"
        )
    return rendered


def show_map(
    output: Callable[[str], object] = print,
    *,
    line_registry: Mapping[str, Sequence[str]] | None = None,
    station_registry: StationRegistry | None = None,
) -> None:
    """Render the metro map through ``output`` (``print`` by default)."""
    for line in render_map(line_registry, station_registry):
        output(line)


def _station_lines(
    line_registry: Mapping[str, Sequence[str]],
) -> dict[str, list[str]]:
    station_lines: dict[str, list[str]] = {}
    for line_name, station_ids in line_registry.items():
        for station_id in station_ids:
            memberships = station_lines.setdefault(station_id, [])
            if line_name not in memberships:
                memberships.append(line_name)
    return station_lines


def _station_label(
    station_id: str,
    station_registry: StationRegistry,
    lines: Sequence[str],
    current_line: str,
) -> str:
    try:
        station = station_registry.get_station(station_id)
    except ValueError:
        label = station_id
    else:
        label = station.name or station_id

    interchange_lines = [line for line in lines if line != current_line]
    if interchange_lines:
        return f"{label} [interchange: {', '.join(interchange_lines)}]"
    return label
