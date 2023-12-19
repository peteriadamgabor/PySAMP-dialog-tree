from sqlalchemy import text, Row

from python.server.database import ITEM_ENGINE


class ItemData:

    def __init__(self, result: Row):
        self._item_id = id
        self._weapon_id: int = result[0]
        self._type: int = result[1]
        self._heal: int = result[2]

    @classmethod
    def new(cls, id: int):
        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT weapon_id, type, heal "
                               "FROM item_data WHERE item_id = :property")
            result: Row | None = conn.execute(query, {'property': id}).one_or_none()

            if result:
                return cls(result)
            return None

    @property
    def weapon_id(self):
        return self._weapon_id

    @property
    def type(self):
        return self._type

    @property
    def heal(self):
        return self._heal
