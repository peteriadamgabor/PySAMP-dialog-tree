import random

from pysamp import set_timer

from python.utils.player import LOGGED_IN_PLAYERS
from python.utils.enums.states import State
from python.utils.enums.colors import Color
from .functions import set_spawn_camera, handle_player_logon, on_vehicle_damage
from .. import exception_logger
from ..utils.vars import VEHICLES, PLAYER_VARIABLES
from ..vehicle.functions import handle_engine_switch
from python.model.server import Vehicle
from python.model.server import Player


@Player.on_request_class
@Player.using_registry
@exception_logger.catch
def on_request_class(player: Player, _):
    pass


@Player.on_connect
@Player.using_registry
@exception_logger.catch
def on_connect(player: Player):
    player.set_color(-1)

    for i in [620, 621, 710, 712, 716, 740, 739, 645]:
        player.remove_building(i, 0.0, 0.0, 0.0, 6000)


@Player.on_disconnect
@Player.using_registry
@exception_logger.catch
def on_disconnect(player: Player, reason: int):
    LOGGED_IN_PLAYERS[player.id] = None
    PLAYER_VARIABLES[player.id] = None


@Player.on_state_change
@Player.using_registry
@exception_logger.catch
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
@exception_logger.catch
def on_exit_vehicle(player: Player, vehicle: Vehicle):
    vehicle = VEHICLES[vehicle.id]

    if vehicle:
        vehicle.remove_passenger(player)
        vehicle.skip_check_damage = True


@Player.on_update
@Player.using_registry
@exception_logger.catch
def on_update(player: Player):
    vehicle: Vehicle = player.get_vehicle()

    if vehicle:

        if vehicle.skip_check_damage:
            vehicle.skip_check_damage = False

        elif player.get_state() == State.DRIVER and vehicle.get_health() != vehicle.health:

            if (damage := round(vehicle.health - vehicle.get_health(), 0)) > 0:
                on_vehicle_damage(player, vehicle, damage)

            vehicle.health = vehicle.get_health()

            if vehicle.is_registered:
                vehicle.update_damage()


@Player.request_download
@Player.using_registry
@exception_logger.catch
def request_download(player: Player, type: int, crc: int):
    return 1


@Player.finished_downloading
@Player.using_registry
@exception_logger.catch
def finished_downloading(player: Player, vw):
    if LOGGED_IN_PLAYERS[player.id] is None:
        player.toggle_spectating(True)
        set_timer(set_spawn_camera, 100, False, player)

        player.game_text("~b~Betöltés folyamatban...", 1500, 3)

        set_timer(handle_player_logon, 1500, False, player)


@Player.on_key_state_change
@Player.using_registry
@exception_logger.catch
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


@Player.on_spawn
@Player.using_registry
@exception_logger.catch
def on_spawn(player: Player):
    player.set_pos(1287.3256, -1528.6997, 13.5457)
    player.set_skin(player.skin.id)


@Player.on_stream_in
@Player.using_registry
@exception_logger.catch
def on_stream_in(player: Player, for_player: Player):
    player.streamed_players.append(for_player)


@Player.on_stream_out
@Player.using_registry
@exception_logger.catch
def on_stream_in(player: Player, for_player: Player):
    for i, p in enumerate(player.streamed_players):
        if p.id == for_player.id:
            del player.streamed_players[i]
