# Panels
import random

from sqlalchemy import text

from python.server.database import MAIN_ENGINE
from python.utils.vars import VEHICLES, VEHICLE_VARIABLES
from python.vehicle.vehicle import Vehicle
from python.vehicle.vehicle_variable import VehicleVariable


@Vehicle.using_registry
def start_engine(vehicle: Vehicle):
    if (600.0 < vehicle.get_health() < 800.0) and random.randint(0, 24) == 12:
        return False

    elif (500.0 < vehicle.get_health() < 600.0) and random.randint(0, 9) == 4:
        return False

    elif (400.0 < vehicle.get_health() < 500.0) and random.randint(0, 1) == 1:
        return False

    elif 400.0 > vehicle.get_health():
        return False

    return True


def reload_vehicle(db_id: int):
    with MAIN_ENGINE.connect() as conn:
        query: text = text("SELECT model_id + 399, x, y, z, angle, color_1, color_2, -1 FROM vehicles WHERE id = :id;")
        data = conn.execute(query, {'id': db_id}).one_or_none()

        veh = Vehicle.create(*data)

        print(f"{veh.id} - reload_vehicle")

        veh.set_number_plate(veh.plate)

        veh.is_registered = True

        VEHICLES[veh.id] = veh

        query: text = text("UPDATE vehicles SET in_game_id = :in_game_id WHERE id = :id;")
        conn.execute(query, {'in_game_id': veh.id, 'id': db_id})
        conn.commit()
