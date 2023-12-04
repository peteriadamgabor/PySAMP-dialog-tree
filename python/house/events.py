from pysamp.dialog import Dialog
from python.house.dialoghandler import handel_for_sale_dialog, handel_owner_dialog, handel_house_guest
from python.house.house import House
from python.pickup.pickup import Pickup
from python.player.player import Player
from python.utils.house import get_house_by_pickup_id


@Player.on_pick_up_pickup
@Player.using_registry
def on_player_pick_up_pickup(player: Player, pickup: Pickup):

    if player.check_block_for_pickup():
        return

    house: House = get_house_by_pickup_id(pickup.id)

    if not house:
        return

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
        name, player_dbid = house.owner

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
