from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Dict

from sqlalchemy import DateTime

from pysamp.player import Player


@dataclass
class PlayerVariable:

    dbid: int

    is_registered: bool = False
    is_logged_in: bool = False
    is_recording: bool = False
    block_for_pickup: bool = False
    used_teleport: bool = False
    in_duty: bool = False
    in_duty_point: bool = False
    login_date: DateTime = datetime.now

    timers: Dict[str, int] = field(default_factory=dict)
    dialog_vars: Dict[str, Any] = field(default_factory=dict)
    check_points: List = field(default_factory=list)
    houses: List = field(default_factory=list)
    custom_vars: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VehicleVariable:
    dbid: int | None

    health: float

    is_starting: bool = False
    is_registered: bool = False
    skip_check_damage: bool = False

    panels_damage_bit: int = 0
    doors_damage_bit: int = 0
    lights_damage_bit: int = 0
    tires_damage_bit: int = 0

    passengers: set[Player] = field(default_factory=set)
    passenger_activity: List[str] = field(default_factory=list)

