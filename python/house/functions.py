from python.model.server import House, Player
from python.utils.enums.colors import Color


def enter_house(player: Player, house: House):
    if house.locked:
        player.send_client_message(Color.RED, "(( A ház zárva van! ))")
        return

    player.set_pos(house.house_type.enter_x, house.house_type.enter_y, house.house_type.enter_z)
    player.set_interior(house.house_type.interior)
    player.set_facing_angle(house.house_type.angle)
    player.set_virtual_world(10_000 + house.id)
    player.set_camera_behind()
