from Cryptodome.Hash import SHA3_512

from pysamp import set_timer, kill_timer
from pysamp.dialog import Dialog
from python.player.dialogs import LOGIN_DIALOG
from python.player.player import Player
from python.utils.colors import Color
from python.utils.player import LOGGED_IN_PLAYERS


def handle_player_logon(player: Player):
    player.game_text("  ", 1000, 2)

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


def set_spawn_camera(args: tuple):
    player = args[0]

    player.set_pos(1122.3563232422, -2036.9317626953, 67)
    player.set_camera_position(1308.4593505859, -2038.3280029297, 102.23148345947)
    player.set_camera_look_at(1122.3563232422, -2036.9317626953, 69.543991088867)


@Player.using_registry
def handel_login_dialog(player: Player, response: int, _, input_text: str) -> None:

    if not bool(response):
        player.kick_with_reason("(( Nem adtál meg jelszót! ))")
        return

    h_obj = SHA3_512.new()
    hash_str = h_obj.update(input_text.encode()).hexdigest()

    if hash_str == player.password:
        kill_timer(player.timers["login_timer"])
        player.set_spawn_info(0, player.skin, 1287.3256, -1528.6997, 13.5457, 0, 0, 0, 0, 0, 0, 0)
        player.toggle_spectating(False)
        LOGGED_IN_PLAYERS[player.id] = player
        player.set_skin(170)
        player.is_logged_in = True
        player.send_client_message(Color.GREEN, "(( Sikeresen bejelentkeztél! ))")

    else:
        player.send_client_message(Color.RED, "(( Hibás jelszó! ))")
        LOGIN_DIALOG.on_response = handel_login_dialog
        player.show_dialog(LOGIN_DIALOG)

    return
