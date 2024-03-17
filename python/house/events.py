from pysamp import callbacks
from python.dialogtree.dialogtree import DialogTree, DialogTreeNode
from python.house.functions import print_house_info, buy_house, enter_house, lock_house, sell_house, cancel_rent, \
    rent_house, extend_rent
from python.model.server import House, Player
from python.utils.enums.dialog_style import DialogStyle
from python.utils.python_helpers import format_numbers


@Player.using_registry
def on_player_pick_up_pickup_house(player: Player, house: House):
    if house is None:
        return 1

    dialog_tree: DialogTree | None = None

    info_node: DialogTreeNode = DialogTreeNode("info_node", DialogStyle.MSGBOX,
                                               "", "", "", "", just_action=True,
                                               custom_handler=print_house_info,
                                               custom_handler_parameters=(house,))

    enter_node: DialogTreeNode = DialogTreeNode("enter_node", DialogStyle.MSGBOX,
                                                "", "", "", "", just_action=True,
                                                custom_handler=enter_house,
                                                custom_handler_parameters=(house,))

    lock_node: DialogTreeNode = DialogTreeNode("lock_node", DialogStyle.MSGBOX,
                                               "", "", "", "", just_action=True,
                                               custom_handler=lock_house,
                                               custom_handler_parameters=(house,))

    player.dialog_vars["house"] = house

    if not house.owner:
        if house.type == 0:
            buy_house_root: DialogTreeNode = DialogTreeNode("no_owner_root", DialogStyle.LIST,
                                                            "Eladó ház", "Információ\nMegvásárlás",
                                                            "Kiválaszt", "Bezár")

            buy_node_content: str = ("{{FFFFFF}}Biztos meg akarja vásárolni a házat {{b4a2da}} " +
                                     format_numbers(house.price + house.house_type.price) +
                                     " {{FFFFFF}}Ft ért?")

            buy_node: DialogTreeNode = DialogTreeNode("buy_node", DialogStyle.MSGBOX,
                                                      "Ház vásárlás", buy_node_content,
                                                      "Megvesz", "Mégsem",
                                                      custom_handler=buy_house,
                                                      custom_handler_parameters=(house,),
                                                      close_in_end=True)

            buy_house_root.add_child(info_node)
            buy_house_root.add_child(buy_node)

            dialog_tree = DialogTree(buy_house_root)

        if house.type == 1:
            rent_house_root: DialogTreeNode = DialogTreeNode("no_rented_root", DialogStyle.LIST,
                                                             "Bérelhető ház", "Információ\nBérlés",
                                                             "Kiválaszt", "Bezár")

            rent_node_content: str = ("{{FFFFFF}}Hány napig szertné bérbe venni a lakást? {{FFFFFF}}\n"
                                      "Ár: {{b4a2da}} " + format_numbers(house.price + house.house_type.price) +
                                      "{{FFFFFF}} Ft / nap ")

            rent_node: DialogTreeNode = DialogTreeNode("rent_node", DialogStyle.INPUT,
                                                       "Ház vásárlás", rent_node_content,
                                                       "Bérlés", "Mégsem",
                                                       custom_handler=rent_house,
                                                       custom_handler_parameters=(house,),
                                                       close_in_end=True,
                                                       stay_if_none=False)

            rent_house_root.add_child(info_node)
            rent_house_root.add_child(rent_node)

            dialog_tree = DialogTree(rent_house_root)
    elif house.owner:
        if house.owner.id == player.dbid:
            if house.type == 0:
                owned_root = DialogTreeNode("owned_root", DialogStyle.LIST,
                                            f"{house.id} ház",
                                            f"Belép\n{'Kinyit' if house.locked else 'Bezár'}\nEladás",
                                            "Kiválaszt", "Bezár")

                sell_node = DialogTreeNode("sell_node", DialogStyle.MSGBOX,
                                           "Ház eladás", "{{FFFFFF}}Biztos elakarod adni a házat {{b4a2da}} "
                                           + format_numbers(house.price + house.house_type.price * .75) +
                                           "{FFFFF}}Ft ért?", "Igen", "Nem",
                                           custom_handler=sell_house,
                                           custom_handler_parameters=(house,))

                owned_root.add_child(enter_node)
                owned_root.add_child(lock_node)
                owned_root.add_child(sell_node)

                dialog_tree = DialogTree(owned_root)
            else:
                rented_root = DialogTreeNode("rented_root", DialogStyle.LIST,
                                             f"{house.id} ház",
                                             f"Belép\n{'Kinyit' if house.locked else 'Bezár'}\n"
                                             f"Bérlés felmondása\nBérleti ido meghosszabítása "
                                             f"{format(house.price, '3_d').replace("_", " ")} Ft/nap Bérlés vége: {house.rent_date:%y-%m-%d}",
                                             "Kiválaszt", "Bezár")

                cancel_rent_node = DialogTreeNode("cancel_rent_node", DialogStyle.MSGBOX,
                                                  f"{house.id} ház",
                                                  "{{FFFFFF}}Biztos leakarod mondai a bérlését?"
                                                  "\nA bérleti díjat nem kapod vissza!", "Igen", "Nem",
                                                  custom_handler=cancel_rent,
                                                  custom_handler_parameters=(house,))

                rent_node_content: str = ("{{FFFFFF}}Hány napig szertné bérbe venni a lakást még? {{FFFFFF}}\n"
                                          "Ár:{{b4a2da}} " + format_numbers(house.price + house.house_type.price) +
                                          "{{FFFFFF}} Ft / nap")

                extend_rent_node = DialogTreeNode("extend_rent_node", DialogStyle.INPUT,
                                                  f"{house.id} ház",
                                                  rent_node_content, "Hosszabítás", "Mégsem",
                                                  custom_handler=extend_rent,
                                                  custom_handler_parameters=(house,),
                                                  back_after_input=True)

                rented_root.add_child(enter_node)
                rented_root.add_child(lock_node)
                rented_root.add_child(cancel_rent_node)
                rented_root.add_child(extend_rent_node)

                dialog_tree = DialogTree(rented_root)
        else:
            guest_root = DialogTreeNode("guest_root", DialogStyle.LIST,
                                        f"{house.id} ház",
                                        "Belép\nInformáció",
                                        "Kiválaszt", "Bezár")

            guest_root.add_child(enter_node)
            guest_root.add_child(info_node)

            dialog_tree = DialogTree(guest_root)

    dialog_tree.show_root_dialog(player)

    return 1
