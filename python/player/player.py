from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy import text

from pysamp.dialog import Dialog
from pysamp.player import Player as BasePlayer
from pysamp import set_timer, get_vehicle_z_angle, call_native_function
import math

from functools import wraps

from .inventory import Inventory
from python.server.database import PLAYER_ENGINE
from python.permission.role import Role
from python.utils.colors import Color
from python.utils.house import get_houses_for_player
from python.utils.vars import VEHICLES, ROLES


class Player(BasePlayer):
    _registry: dict[int, "Player"] = {}
    timers: dict[str, int] = {}
    dialog_vars: Dict[str, Any] = dict()
    _is_registered: bool = False
    _is_logged_in: bool = False
    block_for_pickup: bool = False
    check_points: List = []
    is_recording = False

    def __init__(self, player_id: int):
        super().__init__(player_id)

        self._name = self.get_name()

        with PLAYER_ENGINE.connect() as conn:
            if not self._is_registered:
                query: text = text("SELECT id FROM players WHERE name = :property")
                result = conn.execute(query, {'property': self._name}).fetchone()

                if result:
                    self._dbid: int = result[0]
                    self._is_registered = True

            if not self._is_logged_in and self._is_registered:
                query: text = text("SELECT id, password, money, skin, sex, playedtime, birthdate, role_id FROM players "
                                   "WHERE id = :id")
                result = conn.execute(query, {'id': self._dbid}).fetchone()

                if result:
                    self._password: str = result[1]
                    self._money: float = result[2]
                    self._skin: int = result[3]
                    self._sex: int = result[4]
                    self._playedtime: int = result[5]
                    self._birthdate: datetime.date = result[6]
                    self._inventory: Inventory = Inventory(self)
                    self._role: Role = ROLES[result[7] - 1] if result[7] else None

                    self._houses = get_houses_for_player(self._dbid)

    # region Property

    @property
    def dbid(self):
        return self._dbid

    @property
    def password(self):
        return self._password

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if not self._is_logged_in:
                query: text = text("UPDATE players SET money = :money WHERE id = :id")
                conn.execute(query, {'money': value, "id": self._dbid})
                conn.commit()
                self._money = value

    @property
    def admin(self):
        return self._admin

    @admin.setter
    def admin(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if not self._is_logged_in:
                query: text = text("UPDATE players SET admin = :admin WHERE id = :id")
                conn.execute(query, {'admin': value, "id": self._dbid})
                conn.commit()
                self._admin = value

    @property
    def skin(self):
        return self._skin

    @skin.setter
    def skin(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if not self._is_logged_in:
                query: text = text("UPDATE players SET skin = :skin WHERE id = :id")
                conn.execute(query, {'skin': value, "id": self._dbid})
                conn.commit()
                self._skin = value
                self.set_skin(value)

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if not self._is_logged_in:
                query: text = text("UPDATE players SET birthdate = :birthdate WHERE id = :id")
                conn.execute(query, {'birthdate': value, "id": self._dbid})
                conn.commit()
                self._birthdate = value

    @property
    def playedtime(self):
        return self._birthdate

    @playedtime.setter
    def playedtime(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if not self._is_logged_in:
                query: text = text("UPDATE players SET playedtime = :playedtime WHERE id = :id")
                conn.execute(query, {'playedtime': value, "id": self._dbid})
                conn.commit()
                self._playedtime = value

    @property
    def name(self):
        return self._name.replace("_", " ")

    @property
    def is_registered(self):
        return self._is_registered

    @property
    def is_logged_in(self):
        return self._is_registered

    @is_logged_in.setter
    def is_logged_in(self, value):
        self._is_registered = value

    @property
    def inventory(self):
        return self._inventory

    @property
    def role(self):
        return self._role

    # endregion Property

    # region Functions
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
