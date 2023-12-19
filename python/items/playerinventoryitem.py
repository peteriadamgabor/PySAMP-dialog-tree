from sqlalchemy import text

from python.server.database import ITEM_ENGINE
from python.items.inventory_item import InventoryItem


class PlayerInventoryItem:

    def __init__(self, id: int):
        with (ITEM_ENGINE.connect() as conn):
            query: text = text("SELECT inventory_item_id, amount, worn, dead, in_backpack "
                               "FROM player_inventors WHERE id = :id")
            result = conn.execute(query, {'id': id}).fetchone()

            if result:
                self._id: int = id
                self._inventory_item: InventoryItem = InventoryItem(result[0])
                self._amount: int = result[1]
                self._worn: bool = result[2]
                self._dead: bool = result[3]
                self._in_backpack: bool = result[4]

    # def __del__(self):
    #     with (ITEM_ENGINE.connect() as conn):
    #         query: text = text("DELETE FROM player_inventors WHERE id = :id")
    #         conn.execute(query, {'id': id}).fetchone()

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        with ITEM_ENGINE.connect() as conn:
            query: text = text("UPDATE player_inventors SET amount = :amount WHERE id = :id")
            conn.execute(query, {'amount': value, "id": self._id})
            conn.commit()
            self._amount = value

    @property
    def worn(self):
        return self._worn

    @property
    def dead(self):
        return self._dead

    @property
    def in_backpack(self):
        return self._in_backpack

    # --------------

    @property
    def name(self):
        return self._inventory_item.item.name

    @property
    def max_amount(self):
        return self._inventory_item.item.max_amount

    @property
    def min_price(self):
        return self._inventory_item.item.min_price

    @property
    def max_price(self):
        return self._inventory_item.item.max_price

    @property
    def volume(self):
        return self._inventory_item.item.volume

    @property
    def sellable(self):
        return self._inventory_item.item.sellable

    @property
    def droppable(self):
        return self._inventory_item.item.droppable

    @property
    def data(self):
        return self._inventory_item.item.data

    @property
    def is_stackable(self):
        return self._inventory_item.item.is_stackable

    # --------------

    def use(self):
        return self._inventory_item.item.use()
