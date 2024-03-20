from typing import List

from python.model.database import Skin, Fraction
from python.server.database import MAIN_SESSION


def list_fraction_skins(fraction_id: int, sex: int) -> List[Skin]:
    with MAIN_SESSION() as session:
        fraction: Fraction = session.query(Fraction).filter(Fraction.id == fraction_id).first()
        return [skin for skin in fraction.skins if skin.sex == bool(sex)]
