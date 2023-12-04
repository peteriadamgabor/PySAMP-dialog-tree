from sqlalchemy import text

from python.database import ITEM_ENGINE


class ItemData:

    def __init__(self, id):
        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT weapon_id, type, heal "
                               "FROM item_data WHERE item_id = :property")
            result = conn.execute(query, {'property': id}).fetchone()

            if result:
                self._item_id = id
                self._weapon_id: int = result[0]
                self._type: int = result[1]
                self._heal: int = result[2]

    @property
    def weapon_id(self):
        return self._weapon_id

    @property
    def type(self):
        return self._type

    @property
    def heal(self):
        return self._heal
