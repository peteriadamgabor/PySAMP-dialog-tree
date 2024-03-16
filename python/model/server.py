import math
import datetime
import threading

from typing import List
from functools import wraps
from dataclasses import dataclass

from sqlalchemy import or_

from pysamp.dialog import Dialog
from pysamp.event import event
from pysamp.player import Player as BasePlayer
from pysamp import set_timer, get_vehicle_z_angle, call_native_function
from pystreamer.dynamicobject import DynamicObject
from pystreamer.dynamictextlabel import DynamicTextLabel

from .database import PlayerModel, Skin, PlayerParameter, Fraction, VehicleData, VehicleModel, HouseModel, HouseType, \
    BusinessModel, InteriorModel
from python.server.database import PLAYER_SESSION, VEHICLE_SESSION, HOUSE_SESSION, BUSINESS_SESSION
from python.utils.enums.colors import Color
from python.utils.vars import VEHICLES, PLAYER_VARIABLES, VEHICLE_VARIABLES, PICKUPS, DYNAMIC_PICKUPS, ZONES
from .variable import PlayerVariable, VehicleVariable

from pysamp.pickup import Pickup as BasePickup
from python.utils.enums.pickuptype import PickupType

from python.utils.enums.gate_state import GateState
from pysamp.vehicle import Vehicle as BaseVehicle

from pystreamer.dynamicpickup import DynamicPickup as BaseDynamicPickup
from pystreamer.dynamiczone import DynamicZone as BaseDynamicZone
from ..utils.enums.zone_type import ZoneType


# region Player

class Player(BasePlayer):
    _registry: dict[int, "Player"] = {}

    def __init__(self, player_id: int):
        super().__init__(player_id)

        self._player_vars: PlayerVariable | None = PLAYER_VARIABLES[player_id]

        if self._player_vars is None:
            with PLAYER_SESSION() as session:

                print("1")
                player_db_id = session.query(PlayerModel.id).filter(or_(PlayerModel.in_game_id == player_id,
                                                                    PlayerModel.name == self.get_name())).first()

                print(player_db_id)

                if player_db_id:
                    self.__set_skills()
                    self._player_vars = PlayerVariable(player_db_id[0])
                    self._player_vars.is_registered = True
                    self._player_vars.login_date = datetime.datetime.now()
                    PLAYER_VARIABLES[player_id] = self._player_vars

    # region Property
    @property
    def dbid(self) -> int | None:
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_db_id = session.query(PlayerModel.id).filter(PlayerModel.id == dbid).first()[0]
                return player_db_id
        return None

    @property
    def password(self) -> str | None:
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                password = session.query(PlayerModel.password).filter(PlayerModel.id == dbid).first()[0]
                return password
        return None

    @property
    def money(self) -> float | None:
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                money = session.query(PlayerModel.money).filter(PlayerModel.id == dbid).first()[0]
                return money
        return None

    @money.setter
    def money(self, value: float):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                player_model.money = float(value)
                session.commit()

    @property
    def skin(self) -> Skin | None:
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                return player_model.skin
        return None

    @skin.setter
    def skin(self, value: int):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                skin: Skin = session.query(Skin).filter(Skin.id == value).first()
                super().set_skin(skin.id if skin.dl_id is None else skin.dl_id)
                player_model.skin = skin
                session.commit()

    @property
    def fraction_skin(self) -> Skin | None:

        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_parameter: PlayerParameter = session.query(PlayerParameter).filter(
                    PlayerParameter.player_id == dbid).first()
                return player_parameter.fraction_skin
        return None

    @fraction_skin.setter
    def fraction_skin(self, value):

        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_parameter: PlayerParameter = session.query(PlayerParameter).filter(
                    PlayerParameter.player_id == dbid).first()
                skin: Skin = session.query(Skin).filter(Skin.id == value).first()
                player_parameter.fraction_skin = skin
                player_parameter.fraction_skin_id = skin.id
                session.commit()

    @property
    def fraction(self):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                return player_model.fraction
        return None

    @fraction.setter
    def fraction(self, value):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                fraction: Fraction = session.query(Fraction).filter(Fraction.id == value).first()
                player_model.fraction = fraction
                player_model.fraction_id = fraction.id
                session.commit()

    @property
    def in_duty(self):
        return self._player_vars.in_duty

    @in_duty.setter
    def in_duty(self, value):
        self._player_vars.in_duty = value

    @property
    def in_duty_point(self):
        return self._player_vars.in_duty_point

    @in_duty_point.setter
    def in_duty_point(self, value):
        self._player_vars.in_duty_point = value

    @property
    def sex(self) -> int | None:
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                sex: bool = session.query(PlayerModel.sex).filter(PlayerModel.id == dbid).first()[0]
                return int(sex)
        return None

    @property
    def birthdate(self):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                birthdate: datetime.date = session.query(PlayerModel.birthdate).filter(PlayerModel.id == dbid).first()[
                    0]
                return birthdate
        return None

    @birthdate.setter
    def birthdate(self, value):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                player_model.birthdate = value
                session.commit()

    @property
    def played_time(self):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                played_time: int = session.query(PlayerModel.played_time).filter(PlayerModel.id == dbid).first()[0]
                return played_time
        return None

    @played_time.setter
    def played_time(self, value):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                player_model.played_time = value
                session.commit()

    @property
    def name(self):
        return self.get_name().replace("_", " ")

    @property
    def is_registered(self):
        return self._player_vars.is_registered

    @property
    def is_logged_in(self):
        return self._player_vars.is_logged_in

    @is_logged_in.setter
    def is_logged_in(self, value):
        self._player_vars.is_logged_in = value

    @property
    def items(self):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                return player_model.items
        return None

    @property
    def role(self):
        if self._player_vars is not None:
            dbid: int = self._player_vars.dbid

            with PLAYER_SESSION() as session:
                player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == dbid).first()
                return player_model.role
        return None

    @property
    def timers(self):
        return self._player_vars.timers

    @property
    def check_points(self):
        return self._player_vars.check_points

    @property
    def dialog_vars(self):
        return self._player_vars.dialog_vars

    @property
    def custom_vars(self):
        return self._player_vars.custom_vars

    @property
    def is_recording(self):
        return self._player_vars.is_recording

    @is_recording.setter
    def is_recording(self, value: bool):
        self._player_vars.is_recording = value

    @property
    def block_for_pickup(self):
        return self._player_vars.block_for_pickup

    @block_for_pickup.setter
    def block_for_pickup(self, value: bool):
        self._player_vars.block_for_pickup = value

    @property
    def used_teleport(self):
        return self._player_vars.used_teleport

    @used_teleport.setter
    def used_teleport(self, value: bool):
        self._player_vars.used_teleport = value

    @property
    def login_date(self):
        return self._player_vars.login_date

    # endregion Property

    # region Functions

    def __set_skills(self):
        if not self._player_vars:
            self.set_skill_level(0, 800)
            self.set_skill_level(1, 999)
            self.set_skill_level(2, 999)
            self.set_skill_level(3, 999)
            self.set_skill_level(4, 800)
            self.set_skill_level(5, 999)
            self.set_skill_level(6, 800)
            self.set_skill_level(7, 999)
            self.set_skill_level(8, 999)
            self.set_skill_level(9, 999)
            self.set_skill_level(10, 800)

    def kick_with_reason(self, reason: str, public=True):
        self.send_client_message(Color.RED, reason)
        set_timer(self.kick, 1000, False)

    def get_vehicle(self):
        return VEHICLES[self.get_vehicle_id()]

    def in_vehicle(self) -> bool:
        return VEHICLES[self.get_vehicle_id()] is not None

    def show_dialog(self, dialog: Dialog):
        dialog.show(self)

    def get_x_y_in_front_of_player(self, distance: float) -> tuple[float, float]:
        (x, y, z) = self.get_pos()
        a = self.get_facing_angle()

        if self.is_in_any_vehicle():
            a = get_vehicle_z_angle(self.get_vehicle_id())

        x = x + (distance * math.sin(math.radians(-a)))
        y = y + (distance * math.cos(math.radians(-a)))

        return x, y

    def check_block_for_pickup(self) -> bool:

        if self.block_for_pickup:
            return True

        self.block_for_pickup = True
        set_timer(_enable_pickup, 1000 * 6, False, self)

        return False

    def check_used_teleport(self) -> bool:

        if self._player_vars.used_teleport:
            return True

        self._player_vars.used_teleport = True
        set_timer(_enable_use_teleport, 1000 * 6, False, self)

        return False

    def transfer_money(self, money: int, target: "Player" = None) -> bool:

        if self.money - money < 0:
            self.send_client_message(Color.RED, "(( Nincs elég pénzed! ))")
            return False

        self.money -= money

        if target:
            target.money += money
            target.send_client_message(Color.GREEN, f"(( {self.name} átadott neked {money} Ft-ot. ))")

        return True

    def hide_game_text(self, style):
        call_native_function("HideGameTextForPlayer", self.id, style)

    def set_skin(self, skin_id: int) -> bool:
        with PLAYER_SESSION() as session:
            skin: Skin = session.query(Skin).filter(Skin.id == skin_id).first()
            super().set_skin(skin.id if skin.dl_id is None else skin.dl_id)
            self.skin = skin

    # endregion

    # region Events

    @event("OnPlayerRequestDownload")
    def request_download(cls, player_id: int, type: int, crc):
        return (cls(player_id), type, crc)

    @event("OnPlayerFinishedDownloading")
    def finished_downloading(cls, player_id: int, virtualworld: int):
        return (cls(player_id), virtualworld)

    # endregion

    # region Registry
    @classmethod
    def from_registry_native(cls, player: BasePlayer) -> "Player":
        if isinstance(player, int):
            player_id = player

        if isinstance(player, BasePlayer):
            player_id = player.id

        player = cls._registry.get(player_id)

        if not player:
            cls._registry[player_id] = player = cls(player_id)

        return player

    @classmethod
    def using_registry(cls, func):
        @wraps(func)
        def from_registry(*args, **kwargs):
            args = list(args)
            args[0] = cls.from_registry_native(args[0])
            return func(*args, **kwargs)

        return from_registry

    # endregion


def _enable_pickup(player: Player):
    player.block_for_pickup = False


def _enable_use_teleport(player: Player):
    player.used_teleport = False


# endregion Player

# region Pickup

class Pickup(BasePickup):

    def __init__(self, id: int):
        super().__init__(id)
        self._pickup_type: PickupType | None = None

    @property
    def pickup_type(self) -> PickupType:
        return self._pickup_type

    @pickup_type.setter
    def pickup_type(self, pickup_type: PickupType) -> None:
        self._pickup_type = pickup_type

    def set_model(self, model_id):
        return call_native_function("SetPickupModel", self.id, model_id, True)

    @classmethod
    def create(
            cls,
            model: int,
            type: int,
            x: float,
            y: float,
            z: float,
            virtual_world: int = 0,
            pickup_type: PickupType = None
    ) -> "Pickup":
        super_pickup = super().create(model, type, x, y, z, virtual_world)
        return super_pickup


class DynamicPickup(BaseDynamicPickup):

    def __init__(self, id: int):
        super().__init__(id)
        self._pickup_type: PickupType | None = None

    @property
    def pickup_type(self) -> PickupType:
        return self._pickup_type

    @pickup_type.setter
    def pickup_type(self, pickup_type: PickupType) -> None:
        self._pickup_type = pickup_type

    @classmethod
    def create(
            cls,
            model_id: int,
            type: int,
            x: float,
            y: float,
            z: float,
            world_id: int = -1,
            interior_id: int = -1,
            player_id: int = -1,
            stream_distance: float = 200.0,
            area_id: int = -1,
            priority: int = 0,
    ) -> "DynamicPickup":
        super_pickup = super().create(model_id, type, x, y, z, world_id, interior_id, player_id, stream_distance,
                                      area_id, priority)

        return super_pickup


# endregion Pickup


# region Zone

class DynamicZone(BaseDynamicZone):

    def __init__(self, id: int):
        super().__init__(id)
        self._zone_type: ZoneType | None = None

    @classmethod
    def create_sphere(
            cls,
            x: float,
            y: float,
            z: float,
            size: float,
            world_id: int = -1,
            interior_id: int = -1,
            player_id: int = -1,
            priority: int = 0,
    ) -> "DynamicZone":
        super_zone = super().create_sphere(x, y, z, size, world_id, interior_id, player_id, priority)
        return super_zone

    @property
    def zone_type(self) -> ZoneType:
        return self._zone_type

    @zone_type.setter
    def zone_type(self, zone_type: ZoneType) -> None:
        self._zone_type = zone_type


# endregion Zone

# region Vehicle

class Vehicle(BaseVehicle):
    _registry: dict[int, "Vehicle"] = {}

    def __init__(self, id: int):
        super().__init__(id)

        self._vehicle_variable: VehicleVariable = VEHICLE_VARIABLES[id] if id < len(VEHICLE_VARIABLES) else None

        if self._vehicle_variable is None and id < len(VEHICLE_VARIABLES):
            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.in_game_id == id).first()

                if vehicle_data:
                    health = vehicle_data.health

                    self.set_health(health if health > 250.0 else 250.0)
                    self.set_damage_status(vehicle_data.panels_damage, vehicle_data.doors_damage,
                                           vehicle_data.lights_damage, vehicle_data.tires_damage)

                    self._vehicle_variable: VehicleVariable = VehicleVariable(vehicle_data.id, self.get_health())
                    self._vehicle_variable.is_registered = True

                    VEHICLE_VARIABLES[id] = self._vehicle_variable

                else:
                    self._vehicle_variable: VehicleVariable = VehicleVariable(None, 1000)

    @property
    def dbid(self) -> int:
        return self._vehicle_variable.dbid

    @property
    def model(self) -> VehicleModel:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.model

    @property
    def x(self) -> float:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.x

    @x.setter
    def x(self, value: float):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.x = value
                session.commit()

    @property
    def y(self) -> float:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.y

    @y.setter
    def y(self, value: float):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.y = value
                session.commit()

    @property
    def z(self) -> float:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.z

    @z.setter
    def z(self, value: float):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.z = value
                session.commit()

    @property
    def angle(self) -> float:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.angle

    @angle.setter
    def angle(self, value: float):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.angle = value
                session.commit()

    @property
    def color_1(self) -> int:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.color_1

    @color_1.setter
    def color_1(self, value: int):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.color_1 = value
                session.commit()

    @property
    def color_2(self) -> int:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.color_2

    @color_2.setter
    def color_2(self, value: int):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.color_2 = value
                session.commit()

    @property
    def plate(self) -> str:
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                return vehicle_data.plate

    @plate.setter
    def plate(self, value: str):
        if self._vehicle_variable is not None:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.plate = value
                self.set_number_plate(value)
                session.commit()

    @property
    def health(self) -> float:
        return self._vehicle_variable.health

    @health.setter
    def health(self, value: float):
        if self._vehicle_variable is not None and self.is_registered:
            dbid: int = self._vehicle_variable.dbid

            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()
                vehicle_data.health = float(value)
                session.commit()

        self.set_health(float(value))
        self._vehicle_variable.health = float(value)

    @property
    def skip_check_damage(self) -> bool:
        return self._vehicle_variable.skip_check_damage

    @skip_check_damage.setter
    def skip_check_damage(self, value: bool):
        self._vehicle_variable.skip_check_damage = value

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

    def is_two_wheels(self):
        return self.model.id in [448, 461, 462, 463, 468, 481, 471, 509, 510, 521, 522, 523, 581, 586]

    def add_passenger(self, passenger):
        self._vehicle_variable.passengers.add(passenger)

    def remove_passenger(self, passenger):
        self._vehicle_variable.passengers.remove(passenger)

    def log_passenger_activity(self, passenger, seat):

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

        dbid: int = self._vehicle_variable.dbid
        if dbid is not None:
            with VEHICLE_SESSION() as session:
                vehicle_data: VehicleData = session.query(VehicleData).filter(VehicleData.id == dbid).first()

                vehicle_data.panels_damage = panels
                vehicle_data.doors_damage = doors
                vehicle_data.lights_damage = lights
                vehicle_data.tires_damage = tires
                session.commit()

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


# endregion Vehicle

# region Gate, GateObject

@dataclass
class GateObject:
    model_id: int

    x: float
    y: float
    z: float
    rotation_x: float
    rotation_y: float
    rotation_z: float

    world_id: int
    interior_id: int
    draw_distance: float
    stream_distance: float

    move_x: float
    move_y: float
    move_z: float
    move_rotation_x: float
    move_rotation_y: float
    move_rotation_z: float

    object: DynamicObject = None

    def create_object(self):
        self.object = DynamicObject.create(self.model_id,
                                           self.x,
                                           self.y,
                                           self.z,
                                           self.rotation_x,
                                           self.rotation_y,
                                           self.rotation_z,
                                           world_id=self.world_id,
                                           interior_id=self.interior_id,
                                           draw_distance=self.draw_distance,
                                           stream_distance=self.stream_distance)

    def move_to_open(self, speed: float = 1.0):
        self.object.move(self.move_x, self.move_y, self.move_z, speed,
                         self.move_rotation_x, self.move_rotation_y, self.move_rotation_z)

    def move_to_close(self, speed: float = 1.0):
        self.object.move(self.x, self.y, self.z, speed,
                         self.move_rotation_x, self.move_rotation_y, self.move_rotation_z)


@dataclass
class Gate:
    speed: int
    auto: bool
    close_time: int

    is_opened: bool = False

    state: GateState = GateState(0)
    fractions: List[Fraction] = None
    objects: List[GateObject] = None

    timer: threading.Timer | None = None

    def open(self):
        for gate_object in self.objects:
            gate_object.move_to_open(self.speed)

        if self.auto:
            self.timer = threading.Timer(self.close_time, self.__timed_closed)
            self.timer.start()

    def close(self):
        for gate_object in self.objects:
            gate_object.move_to_close(self.speed)

    def __timed_closed(self):
        for gate_object in self.objects:
            gate_object.move_to_close(self.speed)

        self.timer.cancel()
        self.timer = None


# endregion Gate, GateObject

# region House


class House:

    def __init__(self, id):
        self._id = id

        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == id).first()

            if house_model.owner:
                pickup_model = 1239
            else:
                pickup_model = 1273 if house_model.type == 0 else 1272

            self._pickup: Pickup = Pickup.create(pickup_model, 1, house_model.entry_x, house_model.entry_y,
                                                 house_model.entry_z, 0, PickupType.HOUSE)

            PICKUPS[self._pickup.id] = self._pickup

            self._pickup.pickup_type = PickupType.HOUSE

            self._label: DynamicTextLabel = DynamicTextLabel.create(f"Házszám: {self._id}",
                                                                    Color.LABEL_RED,
                                                                    house_model.entry_x, house_model.entry_y,
                                                                    house_model.entry_z + 0.6,
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
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.entry_x

    @entry_x.setter
    def entry_x(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.entry_x = value
            session.commit()

    @property
    def entry_y(self) -> float:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.entry_y

    @entry_y.setter
    def entry_y(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.entry_y = value
            session.commit()

    @property
    def entry_z(self) -> float:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.entry_z

    @entry_z.setter
    def entry_z(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.entry_z = value
            session.commit()

    @property
    def angle(self) -> float:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.angle

    @angle.setter
    def angle(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.angle = value
            session.commit()

    @property
    def position(self) -> tuple[float, float, float, float]:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.entry_x, house_model.entry_y, house_model.entry_z, house_model.angle

    @position.setter
    def position(self, value: tuple[float, float, float, float]):
        self.entry_x = value[0]
        self.entry_y = value[1]
        self.entry_z = value[2]
        self.angle = value[3]

    @property
    def owner(self):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.owner

    @owner.setter
    def owner(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.owner_id = value
            session.commit()

    @property
    def type(self) -> int:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.type

    @property
    def locked(self) -> bool:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.locked

    @locked.setter
    def locked(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.locked = value
            session.commit()

    @property
    def rent_date(self) -> datetime:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.rent_date

    @rent_date.setter
    def rent_date(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_model.rent_date = value
            session.commit()

    @property
    def house_type(self) -> HouseType:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.house_type

    @house_type.setter
    def house_type(self, value):
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            house_type: HouseType = session.query(HouseType).filter(HouseType.id == self._id).first()

            house_model.house_type_id = house_type.id
            house_model.house_type = house_type
            session.commit()

    @property
    def price(self) -> int:
        with HOUSE_SESSION() as session:
            house_model: HouseModel = session.query(HouseModel).filter(HouseModel.id == self._id).first()
            return house_model.price


# endregion House

# region Interior

class Interior:
    def __init__(self, id: int, x: float, y: float, z: float, interior: int):
        self.id = id
        self.zone = DynamicZone.create_sphere(x, y, z, 1.0, interior_id=interior)
        self.zone.zone_type = ZoneType.BUSINESS_EXIT
        ZONES[self.zone.id] = self.zone

    @property
    def x(self):
        with BUSINESS_SESSION() as session:
            model: InteriorModel = session.query(InteriorModel).filter(InteriorModel.in_game_id == self.id).first()
            return model.x

    @property
    def y(self):
        with BUSINESS_SESSION() as session:
            model: InteriorModel = session.query(InteriorModel).filter(InteriorModel.in_game_id == self.id).first()
            return model.y

    @property
    def z(self):
        with BUSINESS_SESSION() as session:
            model: InteriorModel = session.query(InteriorModel).filter(InteriorModel.in_game_id == self.id).first()
            return model.z

    @property
    def a(self):
        with BUSINESS_SESSION() as session:
            model: InteriorModel = session.query(InteriorModel).filter(InteriorModel.in_game_id == self.id).first()
            return model.a

    @property
    def interior(self):
        with BUSINESS_SESSION() as session:
            model: InteriorModel = session.query(InteriorModel).filter(InteriorModel.in_game_id == self.id).first()
            return model.interior


# endregion

# region Business


class Business:

    def __init__(self, id: int):
        self._id: int = id

        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == id).first()

            self._pickup: DynamicPickup = DynamicPickup.create(1274, 1, model.x, model.y, model.z, 0)

            self._pickup.pickup_type = PickupType.BUSINESS

            DYNAMIC_PICKUPS[self._pickup.id] = self._pickup

            self._label: DynamicTextLabel = DynamicTextLabel.create(model.name, Color.WHITE,
                                                                    model.x, model.y, model.z + 0.6, 25.0)

    @property
    def pickup(self) -> DynamicPickup:
        return self._pickup

    @property
    def label(self) -> DynamicTextLabel:
        return self._label

    @property
    def id(self) -> int:
        return self._id

    @property
    def interior_id(self) -> int:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.interior.in_game_id

    @property
    def name(self) -> str:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.name

    @name.setter
    def name(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.name = value
            session.commit()

    @property
    def entry_x(self) -> float:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.x

    @entry_x.setter
    def entry_x(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.x = value
            session.commit()

    @property
    def entry_y(self) -> float:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.y

    @entry_y.setter
    def entry_y(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.y = value
            session.commit()

    @property
    def entry_z(self) -> float:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.z

    @entry_z.setter
    def entry_z(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.z = value
            session.commit()

    @property
    def angle(self) -> float:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.a

    @angle.setter
    def angle(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.a = value
            session.commit()

    @property
    def owner(self):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.owner

    @owner.setter
    def owner(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.owner_id = value
            session.commit()

    @property
    def business_type_id(self) -> int:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.business_type.id

    @property
    def locked(self) -> bool:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.locked

    @locked.setter
    def locked(self, value):
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            model.locked = value
            session.commit()

    @property
    def price(self) -> int:
        with BUSINESS_SESSION() as session:
            model: BusinessModel = session.query(BusinessModel).filter(BusinessModel.id == self._id).first()
            return model.price

# endregion House
