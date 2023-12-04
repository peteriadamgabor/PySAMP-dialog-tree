from python.utils.vars import ITEMS


def get_item_by_id(item_id: int):
    return next((e for e in ITEMS if e.id == item_id), None)
