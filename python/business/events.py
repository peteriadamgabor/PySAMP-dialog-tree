from python.model.server import Player, Business
from python.utils.vars import INTERIORS


@Player.using_registry
def on_player_pick_up_pickup_business(player: Player, business: Business):
    if business is None:
        return 1

    interior = INTERIORS[business.interior_id]
    player.set_pos(interior.x, interior.y, interior.z)
    player.set_facing_angle(interior.a)
    player.set_interior(interior.interior)
    player.set_virtual_world(20_000 + business.id)
    player.check_used_teleport()

    return 1


