from sqlalchemy import text

from python.database import MAIN_ENGINE
from python.house.house import House
from python.house.housetype import HouseType
from python.utils.vars import HOUSES, HOUSE_TYPES


def server_start():
    load_house_types()
    load_houses()
    load_items()


def load_houses():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM houses")
        ids = conn.execute(query).fetchall()

        print(f"| => Start loging {len(ids)} houses...")

        for id in ids:
            HOUSES.append(House(id[0]))

        print(f"| => Houses are loaded!")


def load_house_types():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM house_types")
        ids = conn.execute(query).fetchall()

        print(f"| => Start loging {len(ids)} house types...")

        for id in ids:
            HOUSE_TYPES.append(HouseType(id[0]))

        print(f"| => House types are loaded!")


def load_items():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM items")
        ids = conn.execute(query).fetchall()

        print(f"| => Start loging {len(ids)} items...")

        for id in ids:
            HOUSE_TYPES.append(HouseType(id[0]))

        print(f"| => Items are loaded!")
