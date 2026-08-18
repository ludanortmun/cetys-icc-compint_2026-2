from metro.station import Station

STATION_REGISTRY: dict[str, Station] = {
}

STATION_ID_TO_IDX: dict[str, int] = { id: idx for idx, id in enumerate(STATION_REGISTRY.keys()) }

STATION_IDX_TO_ID: dict[int, str] = { idx: id for id, idx in STATION_ID_TO_IDX.items() }


LINE_REGISTRY: dict[str, list[str]] = {
    "Red": ["S1", "S2", "S3"],
    "Blue": ["S4", "S5", "S6"],
}
