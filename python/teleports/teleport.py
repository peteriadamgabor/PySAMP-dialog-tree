from dataclasses import dataclass

from pystreamer.dynamiczone import DynamicZone


@dataclass
class Teleport:

    from_x: float
    from_y: float
    from_z: float
    from_interior: int
    from_vw: int
    radius: float
    to_x: float
    to_y: float
    to_z: float
    to_angel: float
    to_interior: int
    to_vw: int
    description: str
    zone: DynamicZone = None


