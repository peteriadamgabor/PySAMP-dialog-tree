import datetime

from python.model.server import House, Player
from python.utils.enums.colors import Color

def print_house_info(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    player.send_client_message(-1, f"|________Fay utca {house.id}________|")

    if house.owner is not None:
        player.send_client_message(-1, f"Tulajdonos: {house.owner.name}")
    else:
        if house.type == 0:
            player.send_client_message(-1, f"Ár: {house.price + house.house_type.price} Ft")
        else:
            player.send_client_message(-1, f"Ár: {house.price + house.house_type.price} Ft / nap")


def buy_house(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    if not player.transfer_money(house.price + house.house_type.price):
        return

    player.send_client_message(Color.GREEN, f"(( Sikeresen megvetted a(z) {{AA3333}}{house.id}{{33AA33}} számú házat!")
    house.pickup.set_model(1239)
    house.owner = player.dbid


@Player.using_registry
def rent_house(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    if not input_text.isdigit():
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")
        return

    if not player.transfer_money((house.price + house.house_type.price) * int(input_text)):
        return

    house.rent_date = datetime.datetime.now() + datetime.timedelta(days=int(input_text))
    house.pickup.set_model(1239)
    house.owner = player.dbid

    player.send_client_message(Color.GREEN, f"(( Sikeresen kibérelted a(z) {{AA3333}}{house.id}{{33AA33}} számú házat!")
    player.send_client_message(Color.GREEN, f"(( {input_text} napra! Bérlés lejárata: {house.rent_date} ))")


def lock_house(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    if house.locked:
        player.send_client_message(Color.GREEN, "(( Sikeresen kinyitottad a házad ))")
        house.locked = False
    else:
        player.send_client_message(Color.GREEN, "(( Sikeresen bezártad a házad ))")
        house.locked = True


def sell_house(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    house.owner = None
    player.send_client_message(Color.GREEN, "(( Sikeresen eladtad a házad! ))")
    player.money += (house.price + house.house_type.price) * .75
    house.pickup.set_model(1273)


def cancel_rent(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    house.owner = None
    player.send_client_message(Color.GREEN, "(( Sikeresen lemondtad a bérlést! ))")
    house.pickup.set_model(1272)


@Player.using_registry
def extend_rent(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    if not input_text.isdigit():
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")

    days = int(input_text)

    if not player.transfer_money((house.price + house.house_type.price) * days):
        return

    house.rent_date += datetime.timedelta(days=days)


def enter_house(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):
    house: House = args[0]

    if house.locked:
        player.send_client_message(Color.RED, "(( A ház zárva van! ))")
        return

    player.set_pos(house.house_type.enter_x, house.house_type.enter_y, house.house_type.enter_z)
    player.set_interior(house.house_type.interior)
    player.set_facing_angle(house.house_type.angle)
    player.set_virtual_world(10_000 + house.id)
    player.set_camera_behind()
