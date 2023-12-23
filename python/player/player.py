from sqlalchemy import text

from pysamp.dialog import Dialog
from pysamp.event import event
from pysamp.player import Player as BasePlayer
from pysamp import set_timer, get_vehicle_z_angle, call_native_function
import math

from functools import wraps

from python.server.database import PLAYER_ENGINE
from python.utils.colors import Color
from python.utils.vars import VEHICLES, PLAYER_VARIABLES, SKINS, FRACTIONS
from .player_variable import PlayerVariable
from .skin import Skin


class Player(BasePlayer):
    _registry: dict[int, "Player"] = {}

    def __init__(self, player_id: int):
        super().__init__(player_id)

        self._player_vars: PlayerVariable = PLAYER_VARIABLES[player_id]

        if not self._player_vars:
            p_vars = PlayerVariable()
            p_vars.load(self.get_name())
            PLAYER_VARIABLES[player_id] = p_vars

    # region Property

    @property
    def dbid(self):
        return self._player_vars.db_id

    @property
    def password(self):
        return self._player_vars.password

    @property
    def money(self):
        return self._player_vars.money

    @money.setter
    def money(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if self._player_vars.is_logged_in:
                query: text = text("UPDATE players SET money = :money WHERE id = :id")
                conn.execute(query, {'money': value, "id": self._player_vars.db_id})
                conn.commit()
                self._player_vars.money = value

    @property
    def skin(self) -> Skin:
        return self._player_vars.skin

    @skin.setter
    def skin(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if self._player_vars.is_logged_in:
                query: text = text("UPDATE players SET skin_id = :skin WHERE id = :id")
                conn.execute(query, {'skin': value, "id": self._player_vars.db_id})
                conn.commit()
                self._player_vars.skin = SKINS[value]
                self.set_skin(self._player_vars.skin.id if self._player_vars.skin.dl_id is None else self._player_vars.skin.dl_id)

    @property
    def fraction_skin(self):
        return self._player_vars.parameter.fraction_skin

    @fraction_skin.setter
    def fraction_skin(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if self._player_vars.is_logged_in:
                query: text = text("UPDATE player_parameters SET fraction_skin_id = :skin WHERE player_id = :id")
                conn.execute(query, {'skin': value, "id": self._player_vars.db_id})
                conn.commit()

                skin = SKINS[value]

                self._player_vars.parameter.fraction_skin = skin

    @property
    def fraction(self):
        return self._player_vars.fraction

    @fraction.setter
    def fraction(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if self._player_vars.is_logged_in:
                query: text = text("UPDATE players SET fraction_id = :fraction_id WHERE player_id = :id")
                conn.execute(query, {'fraction_id': value, "id": self._player_vars.db_id})
                conn.commit()
                self._player_vars.fraction = FRACTIONS[value]

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
    def sex(self) -> int:
        return int(self._player_vars.sex)

    @property
    def birthdate(self):
        return self._player_vars.birthdate

    @birthdate.setter
    def birthdate(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if self._player_vars.is_logged_in:
                query: text = text("UPDATE players SET birthdate = :birthdate WHERE id = :id")
                conn.execute(query, {'birthdate': value, "id": self._player_vars.db_id})
                conn.commit()
                self._player_vars.birthdate = value

    @property
    def playedtime(self):
        return self._player_vars.birthdate

    @playedtime.setter
    def playedtime(self, value):
        with PLAYER_ENGINE.connect() as conn:
            if self._player_vars.is_logged_in:
                query: text = text("UPDATE players SET playedtime = :playedtime WHERE id = :id")
                conn.execute(query, {'playedtime': value, "id": self._player_vars.db_id})
                conn.commit()
                self._player_vars.playedtime = value

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
    def inventory(self):
        return self._player_vars.inventory

    @property
    def role(self):
        return self._player_vars.role

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

    # endregion

    # region Events

    @event("OnPlayerRequestDownload")
    def request_download(cls, playerid: int, type: int, crc):
        return (cls(playerid), type, crc)

    @event("OnPlayerFinishedDownloading")
    def finished_downloading(cls, playerid: int, virtualworld: int):
        return (cls(playerid), virtualworld)

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
