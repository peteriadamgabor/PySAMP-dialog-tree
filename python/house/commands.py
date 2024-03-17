from python.model.server import House
from python.model.server import Player
from python.utils.enums.colors import Color
from python.utils.house import get_house_by_virtual_word


@Player.command(aliases=("kilep",))
@Player.using_registry
def exit(player: Player):

    vw = player.get_virtual_world()

    if vw < 10_000:
        return

    house: House = get_house_by_virtual_word(vw)

    if not house:
        return

    if house.locked:
        player.send_client_message(Color.RED, "(( A ház zárva van!  ))")
        return

    if not player.is_in_range_of_point(5, house.house_type.enter_x, house.house_type.enter_y, house.house_type.enter_z):
        player.send_client_message(Color.RED, "(( Nem vagy az ajtónál! ))")
        return

    player.disable_pickup()
    player.disable_teleport()
    player.set_pos(house.entry_x, house.entry_y, house.entry_z)
    player.set_facing_angle(house.angle)
    player.set_interior(0)
    player.set_virtual_world(0)
    player.set_camera_behind()


@Player.command()
@Player.using_registry
def nyitzar(player: Player):

    vw = player.get_virtual_world()

    if vw < 10_000:
        return

    house: House = get_house_by_virtual_word(vw)

    if not house:
        return

    if not player.is_in_range_of_point(5, house.house_type.enter_x, house.house_type.enter_y, house.house_type.enter_z):
        player.send_client_message(Color.RED, "(( Nem vagy az ajtónál! ))")
        return

    if house.locked:
        player.send_client_message(Color.GREEN, "(( Kinyitottad a házat! ))")
        house.locked = False

    else:
        player.send_client_message(Color.GREEN, "(( Bezártad a házat! ))")
        house.locked = True
