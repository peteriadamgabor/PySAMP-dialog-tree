from enum import Enum


class BusinessTypeEnum(int, Enum):
    NONE = 0  # N/A
    BANK = 1  # BANK
    V_SHOP = 2  # vehicle Shop
    G_SHOP = 3  # Gas Station
    S_SHOP = 4  # Shop
    C_SHOP = 5  # Clothes Shop
    BAR = 6  # Bar
    RESTAURANT = 7  # Restaurant
