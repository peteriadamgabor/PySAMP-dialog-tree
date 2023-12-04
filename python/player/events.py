from pysamp import set_timer

from .functions import set_spawn_camera, handle_player_logon
from .player import Player
from python.utils.player import LOGGED_IN_PLAYERS


@Player.on_request_class
@Player.using_registry
def on_request_class(player: Player, _):
    player.set_color(-1)
    player.toggle_spectating(True)
    set_timer(set_spawn_camera, 500, False, (player,))


@Player.on_connect
@Player.using_registry
def on_connect(player: Player):
    for i in [620, 621, 710, 712, 716, 740, 739, 645]:
        player.remove_building(i, 0.0, 0.0, 0.0, 6000)

    player.game_text("~b~Betoltes folyamatban...", 6000, 3)
    set_timer(handle_player_logon, 1000, False, (player,))


@Player.on_disconnect
@Player.using_registry
def on_disconnect(player: Player, reason: int):
    if player in LOGGED_IN_PLAYERS:
        LOGGED_IN_PLAYERS.remove(player)
