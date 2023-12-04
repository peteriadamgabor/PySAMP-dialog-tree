from sqlalchemy import text

from python.database import ITEM_ENGINE
from .itemdata import ItemData


class Item:

    def __init__(self, id):
        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT name, max_amount, min_price, max_price, "
                               "volume, sellable, droppable "
                               "FROM items WHERE id = :property")
            result = conn.execute(query, {'property': id}).fetchone()

            self._id = id
            self._name: str = result[0]
            self._max_amount: int = result[1]
            self._min_price: int = result[2]
            self._max_price: int = result[3]
            self._volume: bool = result[4]
            self._sellable: bool = result[5]
            self._droppable: bool = result[6]
            self._dead: bool = result[7]
            self._data: ItemData = ItemData(id)

    @property
    def name(self):
        return self._name

    @property
    def max_amount(self):
        return self._max_amount

    @property
    def min_price(self):
        return self._min_price

    @property
    def max_price(self):
        return self._max_price

    @property
    def volume(self):
        return self._volume

    @property
    def sellable(self):
        return self._sellable

    @property
    def droppable(self):
        return self._droppable

    @property
    def data(self):
        return self._data
