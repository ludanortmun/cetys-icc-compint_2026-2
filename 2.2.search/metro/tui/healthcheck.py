"""Render the current service status for every configured metro line."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from metro.network import MetroNetwork
from metro.topology import LINE_REGISTRY

_GREEN = "\033[32m"
_RED = "\033[31m"
_RESET = "\033[0m"


def get_line_closures(
    network: MetroNetwork,
    line_registry: Mapping[str, Sequence[str]] | None = None,
) -> dict[str, list[tuple[str, str]]]:
    """Return the closed consecutive segments for each configured line.

    A closed network segment belongs to a line only when its endpoint IDs are
    adjacent in that line's station list.  This also correctly handles shared
    stations and closed segments that do not belong to any configured line.
    """
    registry = LINE_REGISTRY if line_registry is None else line_registry
    closed_edges = {
        (from_station.id, to_station.id)
        for from_station, to_station in network.get_closed_segments()
    }

    closures_by_line: dict[str, list[tuple[str, str]]] = {}
    for line_name, station_ids in registry.items():
        line_closures: list[tuple[str, str]] = []
        seen_edges: set[tuple[str, str]] = set()
        for from_station_id, to_station_id in zip(station_ids, station_ids[1:]):
            edge = (from_station_id, to_station_id)
            if edge in closed_edges and edge not in seen_edges:
                line_closures.append((from_station_id, to_station_id))
                seen_edges.add(edge)
            reverse_edge = (to_station_id, from_station_id)
            if reverse_edge in closed_edges and reverse_edge not in seen_edges:
                line_closures.append((to_station_id, from_station_id))
                seen_edges.add(reverse_edge)
        closures_by_line[line_name] = line_closures
    return closures_by_line


def render_healthcheck(network: MetroNetwork) -> str:
    """Return an ANSI-coloured status box for the network's configured lines."""
    closures_by_line = get_line_closures(network)
    raw_rows: list[str] = []
    styled_rows: list[str] = []

    for line_name, closures in closures_by_line.items():
        closure_count = len(closures)
        status = (
            "Operational"
            if closure_count == 0
            else f"{closure_count} closed segment"
            f"{'s' if closure_count != 1 else ''}"
        )
        color = _GREEN if closure_count == 0 else _RED
        raw_rows.append(f"{line_name}: ● {status}")
        styled_rows.append(f"{line_name}: {color}● {status}{_RESET}")

    if not raw_rows:
        raw_rows.append("No lines configured")
        styled_rows.append("No lines configured")

    title = "Metro healthcheck"
    width = max(len(title), *(len(row) for row in raw_rows)) + 2
    border = "─" * width
    lines = [
        f"┌{border}┐",
        f"│ {title.ljust(width - 2)} │",
        f"├{border}┤",
    ]
    lines.extend(
        f"│ {styled_row}{' ' * (width - 2 - len(raw_row))} │"
        for raw_row, styled_row in zip(raw_rows, styled_rows)
    )
    lines.append(f"└{border}┘")
    return "\n".join(lines)


def show_healthcheck(network: MetroNetwork) -> None:
    """Print the healthcheck box; suitable for calling from ``main.py``."""
    print(render_healthcheck(network))
