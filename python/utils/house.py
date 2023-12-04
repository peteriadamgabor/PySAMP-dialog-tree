from typing import List

from python.utils.vars import HOUSES, HOUSE_TYPES


def get_house_by_pickup_id(pickup_id: int):
    return next((e for e in HOUSES if e.pickup.id == pickup_id), None)


def get_house_by_virtual_word(vw: int):
    vw -= 10_000
    return next((e for e in HOUSES if e.id == vw), None)


def get_houses_for_player(player_id: int):
    return [e for e in HOUSES if e.owner == player_id]


def get_house_type_by_id(id: int):
    return next((e for e in HOUSE_TYPES if e.id == id), None)
