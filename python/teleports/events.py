from pystreamer.dynamiczone import DynamicZone
from python.player.player import Player
from python.teleports.teleport import Teleport
from python.utils.vars import TELEPORTS


@DynamicZone.on_player_enter
@Player.using_registry
def on_player_enter_dynamic_zone(player: Player, dynamic_zone: DynamicZone):

    player.send_client_message(-1, f"enter {dynamic_zone.id}")

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

    player.send_client_message(-1, f"exit {dynamic_zone.id}")

    if player.fraction and player.fraction.is_valid_duty_point(dynamic_zone.id):
        player.in_duty_point = False
