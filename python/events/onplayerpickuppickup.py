from python.business.events import on_player_pick_up_pickup_business
from python.house.events import on_player_pick_up_pickup_house
from python.model.server import Pickup, Player, DynamicPickup, Business, House
from python.utils.enums.pickuptype import PickupType
from python.utils.vars import PICKUPS, DYNAMIC_PICKUPS, BUSINESSES, HOUSES


@Player.on_pick_up_pickup
@Player.using_registry
def on_pick_up_pickup(player: Player, pickup: Pickup):
    if player.check_block_for_pickup():
        return 1

    pck: Pickup | DynamicPickup = PICKUPS.get(pickup.id)

    if pck is None:
        pck = DYNAMIC_PICKUPS.get(pickup.id)

    match pck.pickup_type:
        case PickupType.HOUSE:
            house: House = HOUSES[pck.id]
            on_player_pick_up_pickup_house(player, house)

        case PickupType.BUSINESS:
            business: Business = BUSINESSES.get(pck.id)
            on_player_pick_up_pickup_business(player, business)

