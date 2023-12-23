import os

from pysamp import on_gamemode_init
from pysamp import set_game_mode_text
from pysamp import on_gamemode_exit

from . import command
from . import utils
from .server import database
from . import player
from . import pickup
from . import house
from .eSelect import eselect

from .server.functions import server_start, set_up_py_samp

@on_gamemode_init
def server_init():
    try:

        # samp.config(encoding="utf-8")

        set_up_py_samp()

        set_game_mode_text("FayRPG 4.0")

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
    pass