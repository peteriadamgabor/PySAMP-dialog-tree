from dataclasses import dataclass
from typing import List

from sqlalchemy import text

from pystreamer.dynamiczone import DynamicZone
from python.fraction.duty_location import DutyLocation
from python.player.skin import Skin
from python.server.database import MAIN_ENGINE
from python.utils.vars import SKINS


@dataclass
class Fraction:
    id: int
    name: str
    acronym: str
    duty_every_where: bool
    skins: List[Skin] = None
    duty_points: List[DutyLocation] = None

    def load_skins(self):
        with MAIN_ENGINE.connect() as conn:
            query: text = text("SELECT skin_id FROM fraction_skins WHERE fraction_id = :property order by id;")
            rows = conn.execute(query, {"property": self.id}).fetchall()

            if len(rows) > 0:
                l_skins = []
                for row in rows:
                    l_skins.append(SKINS[row[0]])

        self.skins = l_skins

    def load_duty_location(self):
        with MAIN_ENGINE.connect() as conn:
            query: text = text("SELECT x, y, z, size, interior, virtual_word FROM fraction_duty_locations "
                               "WHERE fraction_id = :property order by id;")
            rows = conn.execute(query, {"property": self.id}).fetchall()

            if len(rows) > 0:
                self.duty_points = []
                for row in rows:
                    dl = DutyLocation(*row)

                    zone = DynamicZone.create_sphere(dl.x, dl.y, dl.z,
                                                     dl.radius, world_id=dl.vw, interior_id=dl.interior)

                    dl.zone = zone
                    self.duty_points.append(dl)

    def is_valid_duty_point(self, zone_id: int):
        if self.duty_points:
            return next((e for e in self.duty_points if e.zone.id == zone_id), None)

        return None
