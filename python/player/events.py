from pysamp import set_timer, registry

from .functions import set_spawn_camera, handle_player_logon
from python.utils.player import LOGGED_IN_PLAYERS
from .states import State
from ..utils.colors import Color
from ..utils.vars import VEHICLES, PLAYER_VARIABLES
from ..vehicle.vehicle import Vehicle
from pystreamer.dynamiczone import DynamicZone
from python.player.player import Player
from python.teleports.teleport import Teleport
from python.utils.vars import TELEPORTS


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
            vehicle.add_passenger(player)
            vehicle.log_passenger_activity(player.name, player.get_vehicle_seat())

        if not vehicle:
            player.send_client_message(Color.RED, "(( Hibás autó, nincs nyílvántartva! Ezért töröljük az autót... ))")


@Player.on_exit_vehicle
@Player.using_registry
def on_exit_vehicle(player: Player, vehicle: Vehicle):
    vehicle = VEHICLES[vehicle.id]

    if vehicle:
        vehicle.remove_passenger(player)


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


def on_vehicle_damage(player: Player, vehicle: Vehicle, damage: float):
    if damage % 5 == 0:
        return

    match vehicle.model.id:
        case 543 | 605:
            damage *= 1.95

        case 448 | 461 | 462 | 463 | 468 | 471 | 521 | 522 | 523:
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
        veh_player.send_client_message(Color.WHITE, f"Damege: {damage} | lvl: {lvl} ")


@Player.request_download
@Player.using_registry
def request_download(player: Player, type: int, crc: int):
    print('request_download')
    return 1


@Player.finished_downloading
@Player.using_registry
def finished_downloading(player: Player, vw):
    if LOGGED_IN_PLAYERS[player.id] is None:
        player.toggle_spectating(True)
        set_timer(set_spawn_camera, 100, False, player)

        player.game_text("~b~Betoltes folyamatban...", 1500, 3)

        set_timer(handle_player_logon, 1500, False, player)

    print('finished_downloading')


@DynamicZone.on_player_enter
@Player.using_registry
def on_player_enter_dynamic_zone(player: Player, dynamic_zone: DynamicZone):
    teleport: Teleport = TELEPORTS[dynamic_zone.id]
    if teleport:

        if player.check_used_teleport():
            return

        player.set_interior(teleport.to_interior)
        player.set_virtual_world(teleport.to_vw)
        player.set_pos(teleport.to_x, teleport.to_y, teleport.to_z)
        player.set_facing_angle(teleport.to_angel)

    if player.fraction and player.fraction.is_valid_duty_point(dynamic_zone.id):
        player.in_duty_point = True


@DynamicZone.on_player_leave
@Player.using_registry
def on_player_leave_dynamic_zone(player: Player, dynamic_zone: DynamicZone):

    if player.fraction and player.fraction.is_valid_duty_point(dynamic_zone.id):
        player.in_duty_point = False
