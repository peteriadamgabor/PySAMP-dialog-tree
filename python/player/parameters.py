from dataclasses import dataclass

from sqlalchemy import text

from python.player.skin import Skin
from python.server.database import PLAYER_ENGINE
from python.utils.vars import SKINS


@dataclass
class Parameter:
    fraction_skin: Skin = None

    def load(self, db_id: int):
        with PLAYER_ENGINE.connect() as conn:
            query: text = text(
                "SELECT fraction_skin_id  FROM player_parameters"
                " WHERE player_id = :property")
            result = conn.execute(query, {'property': db_id}).one_or_none()

        if result[0]:
            self.fraction_skin = SKINS[result[0]]
