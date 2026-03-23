from dataclasses import dataclass


@dataclass
class Delivery:
    id: int
    x: float
    y: float
    demand: float
    priority: int


@dataclass
class Vehicle:
    id: int
    capacity: float
    max_distance: float