from typing import List

from sqlalchemy import text

from python.database import PLAYER_ENGINE
from python.utils.vars import LOGGED_IN_PLAYERS


def _find_player_by_name(name: str):
    return next((e for e in LOGGED_IN_PLAYERS if name in e.get_name()), None)


def _find_player_by_id(id: int):
    return next((e for e in LOGGED_IN_PLAYERS if e.id == id), None)


def is_valid_player(search_value: str | int):
    if not search_value:
        return None

    if type(search_value) is int:
        return _find_player_by_id(int(search_value))

    if search_value.isdigit():
        return _find_player_by_id(int(search_value))
    else:
        return _find_player_by_name(search_value)


def find_player_in_db_by_name(search_value: str | int):

    if search_value.isdigit():
        return int(search_value)
    else:
        with PLAYER_ENGINE.connect() as conn:
            query: text = text("SELECT id FROM houses WHERE name ILIKE :property'")
            result = conn.execute(query, {'property': id}).fetchall()

            if result == 1:
                return result[0]

            return None
