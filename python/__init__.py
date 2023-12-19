import os

from pysamp import on_gamemode_init
from pysamp import set_game_mode_text
from pysamp import disable_interior_enter_exits
from pysamp import use_player_ped_anims
from pysamp import on_gamemode_exit

from . import command
from . import utils
from .server import database
from . import player
from . import pickup
from . import house

from .server.functions import server_start


@on_gamemode_init
def server_init():
    try:

        # samp.config(encoding="utf-8")

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
