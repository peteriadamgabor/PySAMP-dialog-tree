from sqlalchemy import text

from python.server.database import ITEM_ENGINE
from python.items.item import Item
from python.utils.item import get_item_by_id


class InventoryItem:

    def __init__(self, id):
        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT item_id FROM inventory_items WHERE id = :id")
            result = conn.execute(query, {'id': id}).fetchone()

            if result:
                self._id = id
                self._item: Item = get_item_by_id(result[0])

    # def __del__(self):
    #    with (ITEM_ENGINE.connect() as conn):
    #        query: text = text("DELETE FROM inventory_items WHERE id = :id")
    #        conn.execute(query, {'id': id}).fetchone()

    @property
    def item(self) -> Item:
        return self._item
