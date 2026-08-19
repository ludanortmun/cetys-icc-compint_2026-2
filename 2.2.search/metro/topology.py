from metro.station import Station

ALL_STATIONS: list[Station] = [
    # Green Line
    Station("WBK", "Westbrook"),
    Station("MKS", "Market Square"),
    Station("OKS", "Oak Street"),
    Station("UNS", "Union Square"),
    Station("CVC", "Civic Center"),
    Station("RVP", "Riverside Park"),
    Station("MPW", "Maplewood"),
    Station("KGS", "Kingston"),

    # Blue Line
    Station("HLC", "Hillcrest"),
    Station("PNS", "Pine Street"),
    Station("GAV", "Grand Avenue"),
    Station("UNV", "University"),
    Station("LKS", "Lakeside"),
    Station("HBP", "Harbor Point"),
    Station("MSM", "Museum"),
    
    # Yellow Line
    Station("FND", "Foundry"),
    Station("MDP", "Meadow Park"),

    # Red Line
    Station("MKT", "Market Street"),
    Station("AIR", "Airport"),
]


LINE_REGISTRY: dict[str, list[str]] = {
    "Green": [
        "WBK", "MKS", "OKS", "UNS",
        "CVC", "RVP", "MPW", "KGS",
    ],

    "Blue": [
        "HLC", "PNS", "GAV", "UNS",
        "UNV", "LKS", "HBP", "MSM",
    ],

    "Yellow": [
        "HLC", "GAV", "FND", "MDP",
    ],

    "Red": [
        "FND", "CVC", "MKT", "AIR",
    ],
}