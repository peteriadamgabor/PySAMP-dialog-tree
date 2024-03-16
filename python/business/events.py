from python.model.server import Pickup, Player, DynamicPickup, Business
from python.utils.enums.colors import Color
from python.utils.enums.pickuptype import PickupType
from python.utils.vars import DYNAMIC_PICKUPS, PICKUPS, BUSINESSES, INTERIORS


@Player.on_pick_up_pickup
@Player.using_registry
def on_player_pick_up_pickup(player: Player, pickup: Pickup):
    if player.check_block_for_pickup():
        return

    pck: Pickup | DynamicPickup = PICKUPS.get(pickup.id)

    if pck is None:
        pck = DYNAMIC_PICKUPS.get(pickup.id)

    if pck is None or pck.pickup_type != PickupType.BUSINESS :
        return

    business: Business = BUSINESSES.get(pickup.id)
    player.send_client_message(Color.WHITE, f"{business.name}")

    interior = INTERIORS[business.interior_id]

    player.set_pos(interior.x, interior.y, interior.z)
    player.set_facing_angle(interior.a)
    player.set_interior(interior.interior)
    player.set_virtual_world(20_000 + business.id)
    player.check_used_teleport()
