from typing import Any

from sqlalchemy import text

from python.server.database import HOUSE_ENGINE
from python.pickup.pickup import Pickup
from pystreamer.dynamictextlabel import DynamicTextLabel
from python.utils.colors import Color
from python.utils.house import get_house_type_by_id
from datetime import datetime


class House:

    def __init__(self, id):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("SELECT entry_x, entry_y, entry_z, angle,"
                               "owner_id, type, locked,"
                               "price, housetype_id, rentdate "
                               "FROM houses WHERE id = :property")
            result = conn.execute(query, {'property': id}).fetchone()

            self._id = id
            self._entry_x: float = result[0]
            self._entry_y: float = result[1]
            self._entry_z: float = result[2]
            self._angle: float = result[3]
            self._owner_id: int = result[4]
            self._type: int = result[5]
            self._locked: bool = result[6]
            self._price: int = result[7]
            self._house_type_id: int = result[8]
            self._house_type = get_house_type_by_id(result[8])
            self._rent_date: datetime = result[9]

            if self.owner:
                pickup_model = 1239
            else:
                pickup_model = 1273 if self._type == 0 else 1272

            self._pickup: Pickup = Pickup.create(pickup_model, 1, self._entry_x, self._entry_y, self._entry_z)

            self._label: DynamicTextLabel = DynamicTextLabel.create(f"Házszám: {self._id}",
                                                                    Color.LABEL_RED,
                                                                    self._entry_x, self._entry_y, self._entry_z + 0.6,
                                                                    25.0)

    @property
    def pickup(self) -> Pickup:
        return self._pickup

    @property
    def label(self) -> DynamicTextLabel:
        return self._label

    @property
    def id(self) -> int:
        return self._id

    @property
    def entry_x(self) -> float:
        return self._entry_x

    @entry_x.setter
    def entry_x(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET entry_x = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._entry_x = value

    @property
    def entry_y(self) -> float:
        return self._entry_y

    @entry_y.setter
    def entry_y(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET entry_y = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._entry_y = value

    @property
    def entry_z(self) -> float:
        return self._entry_z

    @entry_z.setter
    def entry_z(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET entry_z = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._entry_z = value

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET angle = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._angle = value

    @property
    def position(self) -> tuple[float, float, float, float]:
        return self._entry_x, self._entry_y, self._entry_z, self._angle

    @position.setter
    def position(self, value: tuple[float, float, float, float]):
        self.entry_x = value[0]
        self.entry_y = value[1]
        self.entry_z = value[2]
        self.angle = value[3]

    @property
    def owner(self):
        if self._owner_id:
            with HOUSE_ENGINE.connect() as conn:
                query: text = text("SELECT name FROM players WHERE id = :property")
                result = conn.execute(query, {'property': self._owner_id}).fetchone()

                return result[0], self._owner_id

        return None

    @owner.setter
    def owner(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET owner_id = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._owner_id = value

    @property
    def type(self) -> int:
        return self._type

    @property
    def locked(self) -> bool:
        return self._locked

    @locked.setter
    def locked(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET locked = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._locked = value

    @property
    def rent_date(self) -> datetime:
        return self._rent_date

    @rent_date.setter
    def rent_date(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET rentdate = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._rent_date = value

    @property
    def house_type(self) -> Any:
        return self._house_type

    @house_type.setter
    def house_type(self, value):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("UPDATE houses SET housetype_id = :value WHERE id = :id")
            conn.execute(query, {'value': value, "id": self._id})
            conn.commit()
            self._house_type_id = value
            self._house_type = get_house_type_by_id(value)

    @property
    def price(self) -> int:
        return self._price
