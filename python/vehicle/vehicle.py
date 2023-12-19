import datetime
from functools import wraps

from sqlalchemy import text

from pysamp.player import Player
from python.server.database import VEHICLE_ENGINE
from python.utils.vars import VEHICLE_MODELS
from python.vehicle.fuletypes import Fuel_Type

from pysamp.vehicle import Vehicle as BaseVehicle
from python.vehicle.vehicle_model import VehicleModel


class Vehicle(BaseVehicle):
    _registry: dict[int, "Vehicle"] = {}

    def __init__(self, id: int):
        super().__init__(id)

        with VEHICLE_ENGINE.connect() as conn:
            query: text = text("SELECT id, model_id, x, y, z, angle, color_1, color_2, fuel_type_id, "
                               "fill_type_id, fuel_level, locked, health, plate "
                               "FROM vehicles WHERE in_game_id = :in_game_id")
            result = conn.execute(query, {'in_game_id': id}).fetchone()

            self._id = id
            self._dbid: int = result[0]
            self._model: VehicleModel = VEHICLE_MODELS[result[1]]
            self._x: float = result[2]
            self._y: float = result[3]
            self._z: float = result[4]
            self._angle: float = result[5]
            self._color_1: int = result[6]
            self._color_2: int = result[7]
            self._fuel_type_id: Fuel_Type = Fuel_Type(result[8])
            self._fill_type_id: Fuel_Type = Fuel_Type(result[9])
            self._fuel_level: float = result[10]
            self._locked: bool = result[11]
            self._health: float = result[12]
            self._plate: str = result[13]

            self._passengers: set[Player] = set()
            self._passenger_activity = []

            self._skip_check_damage = False

    @property
    def model(self) -> VehicleModel:
        return self._model

    @property
    def plate(self) -> str:
        return self._plate

    @property
    def skip_check_damage(self) -> bool:
        return self._skip_check_damage

    @skip_check_damage.setter
    def skip_check_damage(self, value: bool):
        self._skip_check_damage = value

    @property
    def health(self) -> float:
        return self._health

    @health.setter
    def health(self, value: float):
        with VEHICLE_ENGINE.connect() as conn:
            query: text = text("UPDATE vehicles SET health = :health WHERE id = :id")
            conn.execute(query, {'health': value, "id": self._dbid})
            conn.commit()

        self._health = value

    def add_passenger(self, passenger):
        self._passengers.add(passenger)

    def remove_passenger(self, passenger):
        self._passengers.remove(passenger)

    def log_passenger_activity(self, passenger, seat):

        seat_name = ""

        if seat == 128:
            return

        match seat:
            case 0:
                seat_name = "vezetooldali ülés"
            case 1:
                seat_name = "anyos ülés"
            case 2:
                seat_name = "bal hatso ülés"
            case 3:
                seat_name = "jobb hatso ülés"
            case _:
                seat_name = "egyébb ülés"

        self._passenger_activity.append(f"{datetime.datetime.now(datetime.UTC).strftime('%y. %m. %d. %H:%M:%S')} (UTC) - {passenger} - {seat_name}")

    def get_passenger_activity(self):
        return self._passenger_activity

    @property
    def passengers(self):
        return self._passengers

    # region Registry
    @classmethod
    def from_registry_native(cls, vehicle: BaseVehicle) -> "Vehicle":
        if isinstance(vehicle, int):
            vehicle_id = vehicle

        if isinstance(vehicle, BaseVehicle):
            vehicle_id = vehicle.id

        vehicle = cls._registry.get(vehicle_id)

        if not vehicle:
            cls._registry[vehicle_id] = vehicle = cls(vehicle_id)

        return vehicle

    @classmethod
    def using_registry(cls, func):
        @wraps(func)
        def from_registry(*args, **kwargs):
            args = list(args)
            args[0] = cls.from_registry_native(args[0])
            return func(*args, **kwargs)

        return from_registry
    # endregion
