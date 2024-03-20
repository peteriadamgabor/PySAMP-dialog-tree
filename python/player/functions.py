from pysamp import set_timer

from .dialogs import LOGIN_DIALOG
from .events import handel_login_dialog
from python.model.server import Player, Vehicle
from ..utils.enums.colors import Color


def handle_player_logon(player: Player):
    player.hide_game_text(3)

    if player.is_registered:
        LOGIN_DIALOG.on_response = handel_login_dialog
        player.show_dialog(LOGIN_DIALOG)
        player.timers["login_timer"] = set_timer(player.kick_with_reason, 180000, False,
                                                 (
                                                     """((Nem léptél be meghatározott időn belül, "
                                                     "azért a rendszer kirúgott.))""",)
                                                 )

    else:
        player.kick_with_reason("(( Nincs ilyen felhasználó ))")


def set_spawn_camera(player: Player):
    player.set_pos(1122.3563232422, -2036.9317626953, 67)
    player.set_camera_position(1308.4593505859, -2038.3280029297, 102.23148345947)
    player.set_camera_look_at(1122.3563232422, -2036.9317626953, 69.543991088867)


def on_vehicle_damage(player: Player, vehicle: Vehicle, damage: float):
    if damage % 5 == 0 and vehicle.skip_check_damage:
        return

    vehicle.skip_check_damage = True

    match vehicle.get_model():
        case 543 | 605:
            damage *= 1.95

        case 448 | 461 | 462 | 463 | 468 | 481 | 471 | 509 | 510 | 521 | 522 | 523 | 581 | 586:
            damage *= 2.95

        case 528:
            damage *= .35

    for veh_player in vehicle.passengers:
        if damage < 45:
            break

        msg: str
        lvl: float = 2000

        if 45 <= damage <= 69:
            msg = "(( Könnyeben megsérültél! ))"
            lvl += (damage / 3) * 100

        elif 70 <= damage <= 109:
            msg = "(( Súlyosan megsérültél! ))"
            lvl += 2000 + (damage / 3) * 100

        elif 110 <= damage <= 179:
            msg = "(( Életveszélyesen megsérültél! ))"
            lvl += 4000 + (damage / 3) * 100

        else:
            msg = "(( Szörnyethaltál ))"
            lvl = 0

        veh_player.send_client_message(Color.RED, msg)
        veh_player.set_drunk_level(int(lvl))
