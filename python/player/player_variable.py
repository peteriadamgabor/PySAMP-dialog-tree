from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

from sqlalchemy import text

from python.fraction.fraction import Fraction
from python.permission.role import Role
from python.player.inventory import Inventory
from python.player.parameters import Parameter
from python.player.skin import Skin
from python.server.database import PLAYER_ENGINE
from python.utils.house import get_houses_for_player
from python.utils.vars import ROLES, SKINS, FRACTIONS


@dataclass
class PlayerVariable:
    db_id: int = None
    password: str = None
    money: float = None
    skin: Skin = None
    sex: int = None
    played_time: int = None
    birthdate: datetime.date = None
    role: Role = None
    inventory: Inventory = None
    parameter: Parameter = None
    fraction: Fraction = None

    is_registered: bool = False
    is_logged_in: bool = False
    is_recording: bool = False
    block_for_pickup: bool = False
    used_teleport: bool = False
    in_duty: bool = False
    in_duty_point: bool = False

    timers: dict[str, int] = field(default_factory=dict)
    dialog_vars: Dict[str, Any] = field(default_factory=dict)
    check_points: List = field(default_factory=list)
    houses: List = field(default_factory=list)

    def load_player_relations(self, role_id: int | None, fraction_id: int | None):

        self.role = ROLES[role_id - 1] if role_id else None
        self.inventory = Inventory(self.db_id)
        self.houses = get_houses_for_player(self.db_id)
        self.parameter.load(self.db_id)
        self.fraction = FRACTIONS[fraction_id] if fraction_id else None

    def load(self, name):
        with PLAYER_ENGINE.connect() as conn:
            query: text = text(
                "SELECT id, password, money, skin_id, sex, playedtime, birthdate, role_id, fraction_id FROM players"
                " WHERE name = :property")
            result = conn.execute(query, {'property': name}).one_or_none()

            if result:
                self.db_id = result[0]
                self.password = result[1]
                self.money = result[2]
                self.skin = SKINS[result[3]]
                self.sex = result[4]
                self.played_time = result[5]
                self.birthdate = result[6]
                self.is_registered = True
                self.parameter = Parameter()

                self.load_player_relations(result[7], result[8])
