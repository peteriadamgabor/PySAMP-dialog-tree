import random

from Cryptodome.Hash import SHA3_512

from pysamp import set_timer, kill_timer

from python.utils.player import LOGGED_IN_PLAYERS
from .dialogs import LOGIN_DIALOG
from python.utils.enums.states import State
from python.utils.enums.colors import Color
from ..utils.vars import VEHICLES, PLAYER_VARIABLES
from ..vehicle.functions import start_engine
from python.model.server import Vehicle
from python.model.server import Player


@Player.on_request_class
@Player.using_registry
def on_request_class(player: Player, _):
    pass


@Player.on_connect
@Player.using_registry
def on_connect(player: Player):
    player.set_color(-1)

    for i in [620, 621, 710, 712, 716, 740, 739, 645]:
        player.remove_building(i, 0.0, 0.0, 0.0, 6000)


@Player.on_disconnect
@Player.using_registry
def on_disconnect(player: Player, reason: int):
    LOGGED_IN_PLAYERS[player.id] = None
    PLAYER_VARIABLES[player.id] = None


@Player.on_state_change
@Player.using_registry
def on_state_change(player: Player, new_state: int, old_state: int):
    if old_state == State.ON_FOOT and (new_state == State.DRIVER or new_state == State.PASSENGER):
        vehid = player.get_vehicle_id()

        vehicle: Vehicle = VEHICLES[vehid]

        if vehicle:
            vehicle.skip_check_damage = True
            vehicle.add_passenger(player)
            vehicle.log_passenger_activity(player.name, player.get_vehicle_seat())

        if not vehicle.is_registered:
            player.send_client_message(Color.RED, "(( Hibás autó, nincs nyílvántartva! ))")


@Player.on_exit_vehicle
@Player.using_registry
def on_exit_vehicle(player: Player, vehicle: Vehicle):
    vehicle = VEHICLES[vehicle.id]

    if vehicle:
        vehicle.remove_passenger(player)
        vehicle.skip_check_damage = True


@Player.on_update
@Player.using_registry
def on_update(player: Player):
    vehicle: Vehicle = player.get_vehicle()

    if vehicle:

        if vehicle.skip_check_damage:
            vehicle.skip_check_damage = False

        elif player.get_state() == State.DRIVER and vehicle.get_health() != vehicle.health:

            if (damage := round(vehicle.health - vehicle.get_health(), 0)) > 0:
                on_vehicle_damage(player, vehicle, damage)

            vehicle.health = vehicle.get_health()
            vehicle.update_damage()


def on_vehicle_damage(player: Player, vehicle: Vehicle, damage: float):
    if damage % 5 == 0:
        return

    match vehicle.model.id:
        case 543 | 605:
            damage *= 1.95

        case 448 | 461 | 462 | 463 | 468 | 481 | 471 | 509 | 510 | 521 | 522 | 523 | 581 | 586:
            damage *= 2.95

        case 528:
            damage *= .35

    for veh_player in vehicle.passengers:
        if damage < 45:
            break

        msg: str
        lvl: float = 2000

        if 45 <= damage <= 69:
            msg = "(( Könnyeben megsérültél! ))"
            lvl += (damage / 3) * 100

        elif 70 <= damage <= 109:
            msg = "(( Súlyosan megsérültél! ))"
            lvl += 2000 + (damage / 3) * 100

        elif 110 <= damage <= 179:
            msg = "(( Életveszélyesen megsérültél! ))"
            lvl += 4000 + (damage / 3) * 100

        else:
            msg = "(( Szörnyethaltál ))"
            lvl = 0

        veh_player.send_client_message(Color.RED, msg)
        veh_player.set_drunk_level(int(lvl))


@Player.request_download
@Player.using_registry
def request_download(player: Player, type: int, crc: int):
    return 1


@Player.finished_downloading
@Player.using_registry
def finished_downloading(player: Player, vw):
    if LOGGED_IN_PLAYERS[player.id] is None:
        player.toggle_spectating(True)
        set_timer(set_spawn_camera, 100, False, player)

        player.game_text("~b~Betoltes folyamatban...", 1500, 3)

        set_timer(handle_player_logon, 1500, False, player)


@Player.on_key_state_change
@Player.using_registry
def on_key_state_change(player: Player, new_keys: int, old_keys: int):
    if (new_keys == 512 or new_keys == 520) and player.get_state() == State.DRIVER:
        vehicle: Vehicle = player.get_vehicle()
        vehicle.lights = int(not vehicle.lights)

    if new_keys == 640 and player.get_state() == State.DRIVER:
        vehicle: Vehicle = player.get_vehicle()
        handle_engine_switch(player, vehicle)

    if new_keys == 8 and player.get_state() == State.DRIVER:
        number = random.randint(0, 100)
        vehicle: Vehicle = player.get_vehicle()

        if vehicle.get_health() < 450.0 and (70 < number < 85):
            vehicle.engine = 0
            vehicle.get_damage_status()
            player.game_text("~r~Lefulladt az auto", 3000, 3)


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

    player = args[0]
    vehicle = args[1]

    if not start_engine(vehicle):
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

    else:
        vehicle.engine = 1

    vehicle.is_starting = False


def handle_player_logon(player: Player):
    player.game_text("  ", 1000, 2)

    player.hide_game_text(3)

    if player.is_registered:
        LOGIN_DIALOG.on_response = handel_login_dialog
        player.show_dialog(LOGIN_DIALOG)
        player.timers["login_timer"] = set_timer(player.kick_with_reason, 180000, False,
                                                 (
                                                     """((Nem léptél be meghatározott időn belül, "
                                                     "azért a rendszer kirúgott.))""",)
                                                 )

    else:
        player.kick_with_reason("(( Nincs ilyen felhasználó ))")


def set_spawn_camera(player: Player):
    player.set_pos(1122.3563232422, -2036.9317626953, 67)
    player.set_camera_position(1308.4593505859, -2038.3280029297, 102.23148345947)
    player.set_camera_look_at(1122.3563232422, -2036.9317626953, 69.543991088867)


@Player.using_registry
def handel_login_dialog(player: Player, response: int, _, input_text: str) -> None:

    if not bool(response):
        player.kick_with_reason("(( Nem adtál meg jelszót! ))")
        return

    h_obj = SHA3_512.new()
    hash_str = h_obj.update(input_text.encode()).hexdigest()

    if hash_str == player.password:
        kill_timer(player.timers["login_timer"])
        player.is_logged_in = True
        LOGGED_IN_PLAYERS[player.id] = player

        player.set_spawn_info(0, player.skin.id, 1287.3256, -1528.6997, 13.5457, 0, 0, 0, 0, 0, 0, 0)
        player.toggle_spectating(False)
        player.set_skin(player.skin.id)

        player.send_client_message(Color.GREEN, "(( Sikeresen bejelentkeztél! ))")

    else:
        player.send_client_message(Color.RED, "(( Hibás jelszó! ))")
        LOGIN_DIALOG.on_response = handel_login_dialog
        player.show_dialog(LOGIN_DIALOG)
    return
