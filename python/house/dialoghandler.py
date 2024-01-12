import datetime

from pysamp.dialog import Dialog
from python.house.functions import enter_house
from python.model.server import House
from python.model.server import Player
from python.utils.enums.colors import Color
from datetime import date


@Player.using_registry
def handel_for_sale_dialog(player: Player, response: int, list_item: int, input_text: str) -> None:
    if not bool(response):
        return

    list_item = int(list_item)

    house: House | None = player.dialog_vars.get("house", None)

    if not house:
        return

    if list_item == 0:
        player.send_client_message(-1, f"|________Fay utca {house.id}________|")
        player.send_client_message(-1, f"Ár: {format(house.price + house.house_type.price, '3_d').replace("_", " ") + 'Ft' if not house.type == 0 else str(house.price) + 'Ft/nap'}"
                                       f"| Belsõ: {house.house_type.description}")

    if list_item == 1:
        if house.type == 0:
            content: str = ("{{FFFFFF}}Biztos meg akarja vásárolni a házat {{b4a2da}} " +
                            format(house.price + house.house_type.price, '3_d').replace("_", " ") +
                            " {{FFFFFF}}Ft ért?")
            dialog: Dialog = Dialog.create(0, "Eladó ház", content, "Igen", "Nem", on_response=handel_house_buy)
            player.show_dialog(dialog)

        else:

            if not player.transfer_money(house.price + house.house_type.price):
                return

            player.send_client_message(Color.GREEN,f"(( Sikeresen kibérelted a(z) {{AA3333}}{house.id}{{33AA33}} "
                                                   f"számú házat {{AA3333}}1{{33AA33}} napra!")
            house.rent_date = date.today() + datetime.timedelta(days=1)
            house.pickup.set_model(1239)
            house.owner = player.dbid


@Player.using_registry
def handel_house_buy(player: Player, response: int, list_item: int, input_text: str) -> None:
    if not bool(response):
        return

    house: House | None = player.dialog_vars.get("house", None)

    if not player.transfer_money(house.price + house.house_type.price):
        return

    player.send_client_message(Color.GREEN, f"(( Sikeresen megvetted a(z) {{AA3333}}{house.id}{{33AA33}} számú házat!")
    house.pickup.set_model(1239)
    house.owner = player.dbid


@Player.using_registry
def handel_owner_dialog(player: Player, response: int, list_item: int, input_text: str) -> None:
    if not bool(response):
        return

    list_item = int(list_item)

    house: House | None = player.dialog_vars.get("house", None)

    if not house:
        return

    if list_item == 0:
        enter_house(player, house)

    if list_item == 1:
        if house.locked:
            player.send_client_message(Color.GREEN, "(( Sikeresen kinyitottad a házad ))")
            house.locked = False
        else:
            player.send_client_message(Color.GREEN, "(( Sikeresen bezártad a házad ))")
            house.locked = True

    if list_item == 2:
        if house.type == 0:
            content: str = ("{{FFFFFF}}Biztos elakarod adni a házat {{b4a2da}} "
                            + format(house.price + house.house_type.price * .75, '3_d').replace("_", " ") + "{FFFFF}}Ft ért?")
            dialog: Dialog = Dialog.create(0, "Ház eladás", content, "Igen", "Nem", on_response=handel_house_sale)
            player.show_dialog(dialog)

        else:
            content: str = "{{FFFFFF}}Biztos leakarod mondai a bérlését?\n A bérleti díjat nem kapod vissza!"
            dialog: Dialog = Dialog.create(0, "Bérlés felbontása", content, "Igen", "Nem", on_response=handel_house_sale)
            player.show_dialog(dialog)

    if list_item == 3:
        content: str = ("{{FFFFFF}}" + f"A bérlemény {house.rent_date}-ig a tiéd!\n"
                        f"Meghosszíbításhoz ad meg hány nappal akarod meghosszabítani.\n"
                        f"Ár: {format(house.price, '3_d').replace("_", " ")} Ft/nap\n")
        dialog: Dialog = Dialog.create(1, "Bérlés meghosszbítása", content, "Hosszabít", "Nem", on_response=handel_rent_extend)
        player.show_dialog(dialog)


@Player.using_registry
def handel_house_sale(player: Player, response: int, list_item: int, input_text: str) -> None:
    if not bool(response):
        return

    house: House | None = player.dialog_vars.get("house", None)

    if not house:
        return

    if house.type == 0:
        house.owner = None
        player.send_client_message(Color.GREEN, "(( Sikeresen eladtad a házad! ))")
        player.money += (house.price + house.house_type.price) * .75
        house.pickup.set_model(1273)

    else:
        house.owner = None
        player.send_client_message(Color.GREEN, "(( Sikeresen lemondtad a bérlést! ))")
        house.pickup.set_model(1272)


@Player.using_registry
def handel_house_guest(player: Player, response: int, list_item: int, input_text: str):

    if not bool(response):
        return

    list_item = int(list_item)

    house: House | None = player.dialog_vars.get("house", None)

    if not house:
        return

    if list_item == 0:
        enter_house(player, house)

    if list_item == 1:
        player.send_client_message(-1, f"|________Fay utca {house.id}________|")
        player.send_client_message(-1, f"Tulajdonos: {house.owner[0]}")


@Player.using_registry
def handel_rent_extend(player: Player, response: int, list_item: int, input_text: str) -> None:
    if not bool(response):
        return

    house: House | None = player.dialog_vars.get("house", None)

    if not house:
        return

    if not input_text.isdigit():
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")

    days = int(input_text)

    if not player.transfer_money(house.price * days):
        return

    house.rent_date += datetime.timedelta(days=days)

