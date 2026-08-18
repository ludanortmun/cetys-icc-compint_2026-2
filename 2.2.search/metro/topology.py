from metro.station import Station

ALL_STATIONS: list[Station] = [
    Station("S1", "Station 1"),
    Station("S2", "Station 2"),
    Station("S3", "Station 3"), 

    Station("S4", "Station 4"),
    Station("S5", "Station 5"),
    Station("S6", "Station 6"),
]


LINE_REGISTRY: dict[str, list[str]] = {
    "Red": ["S1", "S2", "S3"],
    "Blue": ["S3", "S4", "S5", "S6"],
}
