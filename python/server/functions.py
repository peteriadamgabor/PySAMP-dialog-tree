from sqlalchemy import text

from pysamp import register_callback
from pystreamer import register_callbacks
from pystreamer.dynamiczone import DynamicZone
from python.fraction.fraction import Fraction
from python.permission.command_permission import CommandPermission
from python.permission.permission_type import PermissionType
from python.permission.role import Role
from python.player.skin import Skin
from python.server.database import MAIN_ENGINE
from python.house.house import House
from python.house.housetype import HouseType
from python.items.item import Item
from python.server.console_log import console_log_loading
from python.teleports.teleport import Teleport
from python.utils.vars import HOUSES, HOUSE_TYPES, ITEMS, VEHICLE_MODELS, VEHICLES, PERMISSION_TYPES, ROLES, \
    COMMAND_PERMISSIONS, SKINS, TELEPORTS, FRACTIONS, FRACTIONS_BY_CODE
from python.vehicle.vehicle import Vehicle
from python.vehicle.vehicle_model import VehicleModel


def server_start():

    load_skins()
    load_house_types()
    load_vehicle_models()

    load_houses()
    load_items()
    load_vehicles()

    load_permission_types()
    load_roles()
    load_command_permissions()

    load_teleports()

    load_fractions()


def set_up_py_samp():
    register_callbacks()
    register_callback("OnPlayerFinishedDownloading", "ii")
    register_callback("OnPlayerRequestDownload", "iii")


def load_houses():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM houses;")
        ids = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(ids)} houses...")

        for id in ids:
            HOUSES.append(House(id[0]))

        console_log_loading(f"| => Houses are loaded!")


def load_house_types():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM house_types;")
        ids = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(ids)} house types...")

        for id in ids:
            HOUSE_TYPES.append(HouseType(id[0]))

        console_log_loading(f"| => House types are loaded!")


def load_items():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM items;")
        ids = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(ids)} items...")

        for id in ids:
            ITEMS.append(Item(id[0]))

        console_log_loading(f"| => Items are loaded!")


def load_vehicle_models():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT * FROM vehicle_models;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} vehicle models...")

        for row in rows:
            model = VehicleModel(*row)
            VEHICLE_MODELS[model.id - 399] = model

        console_log_loading(f"| => Vehicle models are loaded!")


def load_vehicles():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id FROM vehicles;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} vehicles...")

        for i in range(len(rows)):
            query: text = text("UPDATE vehicles SET in_game_id = :in_game_id WHERE id = :id;")
            conn.execute(query, {'in_game_id': i + 1, 'id': rows[i][0]})
            conn.commit()

            query: text = text(
                "SELECT model_id + 399, x, y, z, angle, color_1, color_2, 5000 FROM vehicles WHERE id = :id;")
            data = conn.execute(query, {'id': rows[i][0]}).one_or_none()

            veh = Vehicle.create(*data)

            veh.set_number_plate(veh.plate)

            VEHICLES[veh.id] = veh

        console_log_loading(f"| => Vehicles are loaded!")


def load_permission_types():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id, name, code FROM permission_types;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} permission types...")

        for row in rows:
            PERMISSION_TYPES.append(PermissionType(*row))

        console_log_loading(f"| => Permission types are loaded!")


def load_roles():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id, name FROM roles;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} roles...")

        for row in rows:
            ROLES.append(Role(*row))

        console_log_loading(f"| => Roles types are loaded!")


def load_command_permissions():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT cmd_txt, permission_type_id, need_power FROM command_permissions;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} command permissions...")

        for row in rows:
            COMMAND_PERMISSIONS[row[0]] = CommandPermission(*row)

        console_log_loading(f"| => Command permissions types are loaded!")


def load_skins():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT * FROM skins order by id;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} skins...")

        for row in rows:
            SKINS.append(Skin(*row))

        console_log_loading(f"| => Skins are loaded!")


def load_teleports():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT from_x, from_y, from_z, "
                           "from_interior, from_vw, radius, "
                           "to_x, to_y, to_z, to_angel, to_interior, to_vw, description "
                           "FROM teleports order by id;")
        rows = conn.execute(query).fetchall()

        console_log_loading(f"| => Start loging {len(rows)} teleports...")

        for row in rows:
            teleport = Teleport(*row)
            zone = DynamicZone.create_sphere(teleport.from_x, teleport.from_y, teleport.from_z,
                                             1.0, world_id=teleport.from_vw, interior_id=teleport.from_interior)

            teleport.zone = zone

            TELEPORTS[zone.id] = teleport

        console_log_loading(f"| => Teleports are loaded!")


def load_fractions():
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT id, name, acronym FROM fractions order by id;")
        rows = conn.execute(query).all()

        console_log_loading(f"| => Start loging {len(rows)} fractions...")

        for row in rows:
            fraction = Fraction(*row)
            fraction.load_skins()
            FRACTIONS[fraction.id] = fraction
            FRACTIONS_BY_CODE[fraction.acronym] = fraction

        console_log_loading(f"| => fractions are loaded!")

