from typing import List

from sqlalchemy import text

from python.server.database import ITEM_ENGINE
from python.items.playerinventoryitem import PlayerInventoryItem


class Inventory:

    def __init__(self, player):

        self._items: List[PlayerInventoryItem] = []
        self._player = player

        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT id FROM player_inventors WHERE player_id = :id")
            results = conn.execute(query, {'id': player.dbid}).all()

            self._items.extend(PlayerInventoryItem(result[0]) for result in results)

    @property
    def items(self) -> List[PlayerInventoryItem] | None:
        if len(self._items) > 0:
            return self._items

        return None

