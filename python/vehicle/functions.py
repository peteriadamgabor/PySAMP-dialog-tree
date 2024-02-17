# Panels
import random

from sqlalchemy import text

from pysamp import set_timer
from python.server.database import MAIN_ENGINE
from python.utils.enums.colors import Color
from python.utils.enums.states import State
from python.utils.vars import VEHICLES
from python.model.server import Vehicle, Player


def handle_engine_switch(player: Player, vehicle: Vehicle):
    if vehicle.is_starting:
        player.send_client_message(Color.RED, "(( Már indítod! ))")
        return

    if vehicle.engine:
        vehicle.engine = 0
        return

    vehicle.is_starting = True

    if 600.0 <= vehicle.get_health() < 800.0:
        timer_time = 2

    elif 500.0 <= vehicle.get_health() < 600.0:
        timer_time = 5

    elif 400.0 <= vehicle.get_health() < 500.0:
        timer_time = 10

    elif 400.0 >= vehicle.get_health():
        timer_time = 15

    else:
        timer_time = 1

    player.game_text("~w~Inditas...", timer_time * 1000, 3)

    set_timer(do_start_engine, timer_time * 1000, False, (player, vehicle))


def do_start_engine(args):

    player: Player = args[0]
    vehicle: Vehicle = args[1]

    can_start: bool = start_engine(vehicle)

    if not can_start and player.get_state() == State.DRIVER:
        player.game_text("~r~Lefulladt", 3000, 3)
        if 600.0 <= vehicle.get_health() < 800.0:
            player.send_client_message(Color.WHITE, "(( Nem ártana elnézni a szervízbe! ))")

        elif 500.0 <= vehicle.get_health() < 600.0:
            player.send_client_message(Color.WHITE, "(( El kellene menni a szervízbe! ))")

        elif 400.0 <= vehicle.get_health() < 500.0:
            player.send_client_message(Color.WHITE, "(( Surgosen menj szervízbe! ))")

        elif 400.0 >= vehicle.get_health():
            player.send_client_message(Color.WHITE, "(( Hívj szerelot, aki megjavítja a jármuvet! ))")

        vehicle.engine = 0

    elif can_start and player.get_state() == State.DRIVER:
        vehicle.engine = 1

    vehicle.is_starting = False


@Vehicle.using_registry
def start_engine(vehicle: Vehicle) -> bool:
    if (600.0 < vehicle.get_health() < 800.0) and random.randint(0, 24) == 12:
        return False

    elif (500.0 < vehicle.get_health() < 600.0) and random.randint(0, 8) == 4:
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
