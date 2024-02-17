from enum import Enum


class ZoneType(int, Enum):
    TELEPORT = 0
    DUTY_LOCATION = 1
    BUSINESS_EXIT = 2
