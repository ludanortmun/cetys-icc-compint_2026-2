from dataclasses import dataclass


@dataclass(frozen=True)
class Station:
    id: str
    name: str


