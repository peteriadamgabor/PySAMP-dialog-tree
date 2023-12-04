from sqlalchemy import text

from python.database import ITEM_ENGINE
from python.utils.item import get_item_by_id


class InventoryItem:

    def __init__(self, id):
        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT item_id, external_id, externaltype, description, metadata "
                               "FROM inventory_items WHERE inventory_id = :property")
            result = conn.execute(query, {'property': id}).fetchone()

            if result:
                self._inventory = id
                self._item = get_item_by_id(result[0])
                self._external_id: int = result[1]
                self._external_type: int = result[2]
                self._description: int = result[3]
                self._metadata: int = result[4]

    @property
    def item(self):
        return self._item

    @property
    def external_id(self):
        return self._external_id

    @property
    def external_type(self):
        return self._external_type

    @property
    def description(self):
        return self._description


    @property
    def metadata(self):
        return self._metadata
