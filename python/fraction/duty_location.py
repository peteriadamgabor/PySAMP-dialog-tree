from dataclasses import dataclass

from pystreamer.dynamiczone import DynamicZone


@dataclass
class DutyLocation:
    x: float
    y: float
    z: float
    radius: float
    interior: int
    vw: int
    zone: DynamicZone = None
