from typing import List

from python.model.database import Skin
from python.server.database import MAIN_SESSION


def list_skins(sex: int) -> List[Skin]:
    with MAIN_SESSION() as session:
        return session.query(Skin).filter(Skin.sex == bool(sex)).all()
