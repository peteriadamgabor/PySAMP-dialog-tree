from pysamp.dialog import Dialog
from python.house.dialoghandler import handel_for_sale_dialog, handel_owner_dialog, handel_house_guest
from python.model.server import House, Business, DynamicPickup, Pickup, Player
from python.utils.enums.colors import Color
from python.utils.enums.pickuptype import PickupType
from python.utils.vars import PICKUPS, HOUSES, DYNAMIC_PICKUPS, BUSINESSES, INTERIORS


@Player.on_pick_up_pickup
@Player.using_registry
def on_player_pick_up_pickup(player: Player, pickup: Pickup):

    if player.check_block_for_pickup():
        return

    pck: Pickup | DynamicPickup = PICKUPS.get(pickup.id)

    if pck is None:
        pck = DYNAMIC_PICKUPS.get(pickup.id)

    match pck.pickup_type:
        case PickupType.HOUSE:

            house: House = HOUSES[pickup.id]

            player.dialog_vars["house"] = house

            title: str = ""
            content: str = ""
            button1: str = ""
            button2: str = ""
            handler = None

            if not house.owner:
                title = "Eladó ház" if house.type == 0 else "Bérelheto ház"
                content = "Információ\nMegvásárlás" if house.type == 0 else "Információ\nBérlés"
                button1 = "Kiválaszt"
                button2 = "Mégsem"
                handler = handel_for_sale_dialog

            if house.owner:
                name, player_dbid = house.owner.name, house.owner.id

                title = f"{name.replace('_', ' ')} {'tulajdona' if house.type == 0 else 'bérli'}"
                button1 = "Kiválaszt"
                button2 = "Mégsem"

                if player_dbid == player.dbid:
                    content = (f"Belép\n"
                               f"{'Kinyit' if house.locked else 'Bezár'}\n"
                               f"{'Eladás' if house.type == 0 else 'Bérlés felmondása'}"
                               f"{f'\nBérleti ido meghosszabítása {format(house.price, '3_d').replace("_", " ")} Ft/nap' if house.type == 1 else ''}")
                    handler = handel_owner_dialog

                else:
                    content = (f"Belép\n"
                               f"Információ")
                    handler = handel_house_guest

            player.show_dialog(Dialog.create(2, title, content, button1, button2, on_response=handler))

        case PickupType.BUSINESS:
            business: Business = BUSINESSES.get(pickup.id)
            player.send_client_message(Color.WHITE, f"{business.name}")

            interior = INTERIORS[business.interior_id]

            player.set_pos(interior.x, interior.y, interior.z)
            player.set_facing_angle(interior.a)
            player.set_interior(interior.interior)
            player.set_virtual_world(20_000 + business.id)
            player.check_used_teleport()
