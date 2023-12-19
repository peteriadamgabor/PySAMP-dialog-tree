from typing import List

from sqlalchemy import text

from python.server.database import VEHICLE_ENGINE
from python.vehicle.fuletypes import Fuel_Type


class VehicleModel(object):

    def __init__(self, id: int, name: str, real_name: str, seats: int, price: int,
                 trunk_capacity: int, color_number: int, tank_capacity: int,
                 consumption: int, max_speed: int, hood: bool, airbag: bool):

        self._id: int = id
        self._name: str = name
        self._real_name: str = real_name
        self._seats: int = seats
        self._price: int = price
        self._trunk_capacity: int = trunk_capacity
        self._color_number: int = color_number
        self._tank_capacity: int = tank_capacity
        self._consumption: int = consumption
        self._max_speed: int = max_speed
        self._hood: bool = hood
        self._airbag: bool = airbag
        self._allowed_fuel_types: List[Fuel_Type] = self.get_allow_fuel_types()

    def get_allow_fuel_types(self):
        with VEHICLE_ENGINE.connect() as conn:
            query: text = text("SELECT * FROM vehicle_model_fuels "
                               "where vehicle_model_id = :model_id;")
            rows = conn.execute(query, {'model_id': self._id}).fetchall()
            return [Fuel_Type(row[1]) for row in rows]

    @property
    def id(self) -> int:
        return self._id + 399

    @property
    def name(self) -> str:
        return self._name

    @property
    def real_name(self) -> str:
        return self._real_name

    @property
    def seats(self) -> int:
        return self._seats

    @property
    def price(self) -> int:
        return self._price

    @property
    def trunk_capacity(self) -> int:
        return self._trunk_capacity

    @property
    def color_number(self) -> int:
        return self._color_number

    @property
    def tank_capacity(self) -> int:
        return self._tank_capacity

    @property
    def consumption(self) -> int:
        return self._consumption

    @property
    def max_speed(self) -> int:
        return self._max_speed

    @property
    def hood(self) -> bool:
        return self._hood

    @property
    def airbag(self) -> bool:
        return self._airbag

    @property
    def allowed_fuel_types(self) -> List[Fuel_Type]:
        return self._allowed_fuel_types
