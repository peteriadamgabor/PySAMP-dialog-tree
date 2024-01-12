from sqlalchemy import and_

from pystreamer.dynamiczone import DynamicZone
from python.model.database import Teleport, DutyLocation
from python.model.server import Player
from python.server.database import MAIN_SESSION
from python.utils.enums.zone_type import ZoneType
from python.utils.vars import ZONES


@DynamicZone.on_player_enter
@Player.using_registry
def on_player_enter_dynamic_zone(player: Player, dynamic_zone: DynamicZone):
    zone = ZONES.get(dynamic_zone.id)

    match(zone[1]):
        case ZoneType.TELEPORT:
            with MAIN_SESSION() as session:
                teleport = session.query(Teleport).filter(Teleport.in_game_id == dynamic_zone.id).first()

                if teleport and not player.check_used_teleport:
                    player.set_interior(teleport.to_interior)
                    player.set_virtual_world(teleport.to_vw)
                    player.set_pos(teleport.to_x, teleport.to_y, teleport.to_z)
                    player.set_facing_angle(teleport.to_angel)

        case ZoneType.DUTY_LOCATION:
            if player.fraction is not None:
                with MAIN_SESSION() as session:
                    duty_location = session.query(DutyLocation).filter(and_(DutyLocation.in_game_id == dynamic_zone.id,
                                                                            DutyLocation.fraction_id == player.fraction.id)).first()

                    if duty_location:
                        player.send_client_message(-1, "Duty Point")
                        player.in_duty_point = True


@DynamicZone.on_player_leave
@Player.using_registry
def on_player_leave_dynamic_zone(player: Player, dynamic_zone: DynamicZone):
    if player.in_duty_point:
        player.in_duty_point = False
