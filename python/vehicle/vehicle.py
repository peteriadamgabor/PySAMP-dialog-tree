import datetime
from functools import wraps

from sqlalchemy import text

from pysamp.player import Player
from python.server.database import VEHICLE_ENGINE
from python.utils.vars import VEHICLE_MODELS, VEHICLE_VARIABLES
from python.vehicle.fuletypes import Fuel_Type

from pysamp.vehicle import Vehicle as BaseVehicle
from python.vehicle.vehicle_model import VehicleModel
from python.vehicle.vehicle_variable import VehicleVariable


class Vehicle(BaseVehicle):
    _registry: dict[int, "Vehicle"] = {}

    def __init__(self, id: int):
        super().__init__(id)

        self._vehicle_variable: VehicleVariable = VEHICLE_VARIABLES[id]

        if not self._vehicle_variable:

            self._vehicle_variable: VehicleVariable = VehicleVariable()

            VEHICLE_VARIABLES[id] = self._vehicle_variable

            with VEHICLE_ENGINE.connect() as conn:
                query: text = text("SELECT id, model_id, x, y, z, angle, color_1, color_2, fuel_type_id, "
                                   "fill_type_id, fuel_level, locked, health, plate "
                                   "FROM vehicles WHERE in_game_id = :in_game_id")
                result = conn.execute(query, {'in_game_id': id}).fetchone()

                self._vehicle_variable.db_id = result[0]
                self._vehicle_variable.model = VEHICLE_MODELS[result[1]]
                self._vehicle_variable.x = result[2]
                self._vehicle_variable.y = result[3]
                self._vehicle_variable.z = result[4]
                self._vehicle_variable.angle = result[5]
                self._vehicle_variable.color_1 = result[6]
                self._vehicle_variable.color_2 = result[7]
                self._vehicle_variable.fuel_type_id = Fuel_Type(result[8])
                self._vehicle_variable.fill_type_id = Fuel_Type(result[9])
                self._vehicle_variable.fuel_level = result[10]
                self._vehicle_variable.locked = result[11]
                self._vehicle_variable.health = result[12]
                self._vehicle_variable.plate = result[13]

                self._vehicle_variable.passengers = set()
                self._vehicle_variable.passenger_activity = []

                self._vehicle_variable.skip_check_damage = False

    @property
    def model(self) -> VehicleModel:
        return self._vehicle_variable.model

    @property
    def plate(self) -> str:
        return self._vehicle_variable.plate

    @property
    def skip_check_damage(self) -> bool:
        return self._vehicle_variable.skip_check_damage

    @skip_check_damage.setter
    def skip_check_damage(self, value: bool):
        self._vehicle_variable.skip_check_damage = value

    @property
    def health(self) -> float:
        return self._vehicle_variable.health

    @health.setter
    def health(self, value: float):
        with VEHICLE_ENGINE.connect() as conn:
            query: text = text("UPDATE vehicles SET health = :health WHERE id = :id")
            conn.execute(query, {'health': value, "id": self._vehicle_variable.db_id})
            conn.commit()

        self._vehicle_variable.health = value

    def add_passenger(self, passenger):
        self._vehicle_variable.passengers.add(passenger)

    def remove_passenger(self, passenger):
        self._vehicle_variable.passengers.remove(passenger)

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

        self._vehicle_variable.passenger_activity.append(f"{datetime.datetime.now(datetime.UTC).strftime('%Y. %m. %d. %H:%M:%S')} (UTC) - {passenger} - {seat_name}")

    def get_passenger_activity(self):
        return self._vehicle_variable.passenger_activity

    @property
    def passengers(self):
        return self._vehicle_variable.passengers

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
