from ..model.database import Item
from ..server.database import PLAYER_SESSION


def is_valid_item_id(item_id: int) -> bool:
    with PLAYER_SESSION() as session:
        return session.query(Item).filter(Item.id == item_id).first() is not None
