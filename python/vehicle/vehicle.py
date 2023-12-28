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

        self._vehicle_variable: VehicleVariable = VEHICLE_VARIABLES[id] if id < len(VEHICLE_VARIABLES) else None

        if not self._vehicle_variable and id < len(VEHICLE_VARIABLES):

            self._vehicle_variable: VehicleVariable = VehicleVariable()

            VEHICLE_VARIABLES[id] = self._vehicle_variable

            self._vehicle_variable.model = VEHICLE_MODELS[self.get_model() - 399]

            with VEHICLE_ENGINE.connect() as conn:
                query: text = text("SELECT id, model_id, x, y, z, angle, color_1, color_2, fuel_type_id, "
                                   "fill_type_id, fuel_level, locked, health, plate,"
                                   "panels_damage, doors_damage, lights_damage, tires_damage "
                                   "FROM vehicles WHERE in_game_id = :in_game_id")
                result = conn.execute(query, {'in_game_id': id}).fetchone()

                if result is not None:
                    self._vehicle_variable.db_id = result[0]
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

                    self.set_health(result[12] if result[12] > 250.0 else 250.0)
                    self.set_damage_status(result[14], result[15], result[16], result[17])

    @property
    def db_id(self) -> int:
        return self._vehicle_variable.db_id

    @property
    def model(self) -> VehicleModel:
        return self._vehicle_variable.model

    @property
    def x(self) -> float:
        return self._vehicle_variable.x

    @x.setter
    def x(self, value: float):
        self._vehicle_variable.x = value

    @property
    def y(self) -> float:
        return self._vehicle_variable.y

    @y.setter
    def y(self, value: float):
        self._vehicle_variable.y = value

    @property
    def z(self) -> float:
        return self._vehicle_variable.z

    @z.setter
    def z(self, value: float):
        self._vehicle_variable.z = value

    @property
    def angle(self) -> float:
        return self._vehicle_variable.angle

    @angle.setter
    def angle(self, value: float):
        self._vehicle_variable.angle = value

    @property
    def color_1(self) -> int:
        return self._vehicle_variable.color_1

    @color_1.setter
    def color_1(self, value: int):
        self._vehicle_variable.color_1 = value

    @property
    def color_2(self) -> int:
        return self._vehicle_variable.color_2

    @color_2.setter
    def color_2(self, value: int):
        self._vehicle_variable.color_2 = value


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

        value = float(value)

        with VEHICLE_ENGINE.connect() as conn:
            query: text = text("UPDATE vehicles SET health = :health WHERE id = :id")
            conn.execute(query, {'health': value, "id": self._vehicle_variable.db_id})
            conn.commit()

        self.set_health(value)
        self._vehicle_variable.health = value

    @property
    def is_registered(self) -> float:
        return self._vehicle_variable.is_registered

    @is_registered.setter
    def is_registered(self, value: bool):
        self._vehicle_variable.is_registered = value

    @property
    def is_starting(self) -> float:
        return self._vehicle_variable.is_starting

    @is_starting.setter
    def is_starting(self, value: bool):
        self._vehicle_variable.is_starting = value

    @property
    def engine(self):
        engine, _, _, _, _, _, _ = self.get_params_ex()
        return engine

    @engine.setter
    def engine(self, value: int):
        _, lights, alarm, doors, bonnet, boot, objective = self.get_params_ex()
        self.set_params_ex(value, lights, alarm, doors, bonnet, boot, objective)

    @property
    def lights(self):
        _, lights, _, _, _, _, _ = self.get_params_ex()
        return lights

    @lights.setter
    def lights(self, value: int):
        engine, _, alarm, doors, bonnet, boot, objective = self.get_params_ex()
        self.set_params_ex(engine, value, alarm, doors, bonnet, boot, objective)

    @property
    def alarm(self):
        _, _, alarm, _, _, _, _ = self.get_params_ex()
        return alarm

    @alarm.setter
    def alarm(self, value: int):
        engine, lights, _, doors, bonnet, boot, objective = self.get_params_ex()
        self.set_params_ex(engine, lights, value, doors, bonnet, boot, objective)

    @property
    def doors(self):
        _, _, _, doors, _, _, _ = self.get_params_ex()
        return doors

    @doors.setter
    def doors(self, value: int):
        engine, lights, alarm, _, bonnet, boot, objective = self.get_params_ex()
        self.set_params_ex(engine, lights, alarm, value, bonnet, boot, objective)

    @property
    def hood(self):
        _, _, _, _, bonnet, _, _ = self.get_params_ex()
        return bonnet

    @hood.setter
    def hood(self, value: int):
        engine, lights, alarm, doors, _, boot, objective = self.get_params_ex()
        self.set_params_ex(engine, lights, alarm, doors, value, boot, objective)

    @property
    def trunk(self):
        _, _, _, _, _, boot, _ = self.get_params_ex()
        return boot

    @trunk.setter
    def trunk(self, value: int):
        engine, lights, alarm, doors, bonnet, _, objective = self.get_params_ex()
        self.set_params_ex(engine, lights, alarm, doors, bonnet, value, objective)

    def update_damage(self):

        panels, doors, lights, tires = self.get_damage_status()

        if (self._vehicle_variable.panels_damage_bit == panels
                and self._vehicle_variable.doors_damage_bit == doors
                and self._vehicle_variable.lights_damage_bit == lights
                and self._vehicle_variable.tires_damage_bit == tires):
            return

        with VEHICLE_ENGINE.connect() as conn:
            query: text = text("UPDATE vehicles SET panels_damage = :panels_damage, "
                               "doors_damage = :doors_damage, lights_damage = :lights_damage, "
                               "tires_damage = :tires_damage WHERE id = :id")
            conn.execute(query, {'panels_damage': panels,
                                 'doors_damage': doors,
                                 'lights_damage': lights,
                                 'tires_damage': tires,
                                 "id": self._vehicle_variable.db_id})
            conn.commit()

        self._vehicle_variable.panels_damage_bit = panels
        self._vehicle_variable.doors_damage_bit = doors
        self._vehicle_variable.lights_damage_bit = lights
        self._vehicle_variable.tires_damage_bit = tires

    def load_damage(self):
        self.set_damage_status(self._vehicle_variable.panels_damage_bit,
                               self._vehicle_variable.doors_damage_bit,
                               self._vehicle_variable.lights_damage_bit,
                               self._vehicle_variable.tires_damage_bit)
        self.update_damage()

    def get_panels_damage(self):
        return decode_panels(self._vehicle_variable.panels_damage_bit)

    def get_doors_damage(self):
        return decode_doors(self._vehicle_variable.doors_damage_bit)

    def get_lights_damage(self):
        return decode_lights(self._vehicle_variable.lights_damage_bit)

    def get_tires_damage(self):
        return decode_tires(self._vehicle_variable.tires_damage_bit)

    def update_panels_damage(self, front_left_panel,
                             front_right_panel,
                             rear_left_panel,
                             rear_right_panel,
                             windshield,
                             front_bumper,
                             rear_bumper):
        _, doors, lights, tires = self.get_damage_status()

        panels = encode_panels(front_left_panel,
                               front_right_panel,
                               rear_left_panel,
                               rear_right_panel,
                               windshield,
                               front_bumper,
                               rear_bumper)

        self.set_damage_status(panels, doors, lights, tires)
        self.update_damage()

    def update_doors_damage(self, bonnet, boot, driver_door, passenger_door):
        panels, _, lights, tires = self.get_damage_status()

        doors = encode_doors(bonnet, boot, driver_door, passenger_door)

        self.set_damage_status(panels, doors, lights, tires)
        self.update_damage()

    def update_lights_damage(self, front_left_light, front_right_light, back_lights):
        panels, doors, _, tires = self.get_damage_status()

        lights = encode_lights(front_left_light, front_right_light, back_lights)

        self.set_damage_status(panels, doors, lights, tires)
        self.update_damage()

    def update_tires_damage(self, rear_right_tire, front_right_tire, rear_left_tire, front_left_tire):
        panels, doors, lights, _ = self.get_damage_status()

        tires = encode_tires(rear_right_tire, front_right_tire, rear_left_tire, front_left_tire)

        self.set_damage_status(panels, doors, lights, tires)
        self.update_damage()

    def is_two_wheels(self):
        return self.model.id in [448, 461, 462, 463, 468, 481, 471, 509, 510, 521, 522, 523, 581, 586]

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

        self._vehicle_variable.passenger_activity.append(
            f"{datetime.datetime.now(datetime.UTC).strftime('%Y. %m. %d. %H:%M:%S')} (UTC) - {passenger} - {seat_name}")

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


def decode_panels(panels) -> tuple[int, int, int, int, int, int, int]:
    front_left_panel = panels & 15
    front_right_panel = (panels >> 4) & 15
    rear_left_panel = (panels >> 8) & 15
    rear_right_panel = (panels >> 12) & 15
    windshield = (panels >> 16) & 15
    front_bumper = (panels >> 20) & 15
    rear_bumper = (panels >> 24) & 15
    return front_left_panel, front_right_panel, rear_left_panel, rear_right_panel, windshield, front_bumper, rear_bumper


def encode_panels(front_left_panel, front_right_panel, rear_left_panel, rear_right_panel, windshield, front_bumper,
                  rear_bumper):
    return front_left_panel | (front_right_panel << 4) | (rear_left_panel << 8) | (rear_right_panel << 12) | (
            windshield << 16) | (front_bumper << 20) | (rear_bumper << 24)


# Doors
def decode_doors(doors):
    bonnet = doors & 7
    boot = (doors >> 8) & 7
    driver_door = (doors >> 16) & 7
    passenger_door = (doors >> 24) & 7
    return bonnet, boot, driver_door, passenger_door


def encode_doors(bonnet, boot, driver_door, passenger_door):
    return bonnet | (boot << 8) | (driver_door << 16) | (passenger_door << 24)


# Lights
def decode_lights(lights):
    front_left_light = lights & 1
    front_right_light = (lights >> 2) & 1
    back_lights = (lights >> 6) & 1
    return front_left_light, front_right_light, back_lights


def encode_lights(front_left_light, front_right_light, back_lights):
    return front_left_light | (front_right_light << 2) | (back_lights << 6)


# Tires
def decode_tires(tires):
    rear_right_tire = tires & 1
    front_right_tire = (tires >> 1) & 1
    rear_left_tire = (tires >> 2) & 1
    front_left_tire = (tires >> 3) & 1
    return rear_right_tire, front_right_tire, rear_left_tire, front_left_tire


def encode_tires(rear_right_tire, front_right_tire, rear_left_tire, front_left_tire):
    return rear_right_tire | (front_right_tire << 1) | (rear_left_tire << 2) | (front_left_tire << 3)
