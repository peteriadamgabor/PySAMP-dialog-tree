from sqlalchemy import and_

from python.model.database import Teleport, DutyLocation
from python.model.server import Player, DynamicZone, Business
from python.server.database import MAIN_SESSION
from python.utils.enums.zone_type import ZoneType
from python.utils.vars import ZONES, BUSINESSES, INTERIORS


@DynamicZone.on_player_enter
@Player.using_registry
def on_player_enter_dynamic_zone(player: Player, dynamic_zone: DynamicZone):
    zone: DynamicZone = ZONES.get(dynamic_zone.id)

    if not zone:
        return

    match zone.zone_type:
        case ZoneType.TELEPORT:
            with MAIN_SESSION() as session:
                teleport = session.query(Teleport).filter(Teleport.in_game_id == dynamic_zone.id).first()

                if teleport:
                    player.set_interior(teleport.to_interior)
                    player.set_virtual_world(teleport.to_vw)
                    player.set_pos(teleport.to_x, teleport.to_y, teleport.to_z)
                    player.set_facing_angle(teleport.to_angel)

        case ZoneType.DUTY_LOCATION:
            if player.fraction is not None:
                with (MAIN_SESSION() as session):
                    duty_location = session.query(DutyLocation).filter(
                        and_(DutyLocation.in_game_id == dynamic_zone.id,
                             DutyLocation.fraction_id == player.fraction.id)
                    ).first()

                    if duty_location:
                        player.in_duty_point = True

        case ZoneType.BUSINESS_EXIT:
            if not player.check_used_teleport():
                business: Business = BUSINESSES.get(player.get_virtual_world() - 20_000)

                player.set_pos(business.entry_x, business.entry_y, business.entry_z)
                player.set_facing_angle(business.angle)
                player.set_interior(0)
                player.set_virtual_world(0)


@DynamicZone.on_player_leave
@Player.using_registry
def on_player_leave_dynamic_zone(player: Player, dynamic_zone: DynamicZone):
    if player.in_duty_point:
        player.in_duty_point = False
