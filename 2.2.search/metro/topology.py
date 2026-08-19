from metro.station import Station

ALL_STATIONS: list[Station] = [
    # Green Line
    Station("S1", "Westbrook"),
    Station("S2", "Market Square"),
    Station("S3", "Oak Street"),
    Station("S4", "Union Square"),
    Station("S5", "Civic Center"),
    Station("S6", "Riverside Park"),
    Station("S7", "Maplewood"),
    Station("S8", "Kingston"),

    # Blue Line
    Station("S9", "Hillcrest"),
    Station("S11", "Pine Street"),
    Station("S10", "Grand Avenue"),
    Station("S12", "University"),
    Station("S13", "Lakeside"),
    Station("S14", "Harbor Point"),
    Station("S15", "Museum"),
    
    # Yellow Line
    Station("S16", "Foundry"),
    Station("S17", "Meadow Park"),

    # Red Line
    Station("S18", "Market Street"),
    Station("S19", "Airport"),
]


LINE_REGISTRY: dict[str, list[str]] = {
    "Green": [
        "S1", "S2", "S3", "S4",
        "S5", "S6", "S7", "S8",
    ],

    "Blue": [
        "S9", "S11", "S10", "S4",
        "S12", "S13", "S14", "S15",
    ],

    "Yellow": [
        "S9", "S10", "S16", "S17",
    ],

    "Red": [
        "S16", "S5", "S18", "S19",
    ],
}