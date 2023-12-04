import os

from pysamp import on_gamemode_init, set_game_mode_text, disable_interior_enter_exits, use_player_ped_anims, \
    on_gamemode_exit
from . import command
from . import utils
from . import database
from . import player
from . import pickup
from . import house
import samp

from .server.functions import server_start


@on_gamemode_init
def server_init():
    try:
        samp.config(encoding="cp1252")

        set_game_mode_text("FayRPG 4.0")
        disable_interior_enter_exits()
        use_player_ped_anims()

        print("+----------------------------------------+")
        print("|     Start populate server entities     |")
        print("+----------------------------------------+")

        server_start()

        print("+----------------------------------------+")
        print("|     Population is finish successful    |")
        print("+----------------------------------------+")

    except Exception as ex:
        print("===================================================================\n"
              "        Something want wrong in server start up \n"
              "===================================================================\n")
        raise ex


@on_gamemode_exit
def server_exit():
    print("stop")
    os.remove("../log.txt")
