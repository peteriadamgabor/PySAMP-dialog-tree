from dataclasses import dataclass, field
from typing import List

from python.player.player import Player
from python.vehicle.fuletypes import Fuel_Type
from python.vehicle.vehicle_model import VehicleModel


@dataclass
class VehicleVariable:
    db_id: int = None
    model: VehicleModel = None
    x: float = None
    y: float = None
    z: float = None
    angle: float = None
    color_1: int = None
    color_2: int = None
    fuel_type_id: Fuel_Type = None
    fill_type_id: Fuel_Type = None
    fuel_level: float = None
    locked: bool = None
    health: float = None
    plate: str = None

    passengers: set[Player] = field(default_factory=set)
    passenger_activity: List[str] = field(default_factory=list)

    skip_check_damage: bool = False
