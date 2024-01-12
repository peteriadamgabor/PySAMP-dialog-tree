from pysamp import on_gamemode_init, on_gamemode_exit

from .model import database
from .server import database
from .zone import events
from . import command
from . import utils
from . import player
from . import house
from . import vehicle

from .server.functions import server_start, set_up_py_samp

@on_gamemode_init
def server_init():
    try:

        # samp.config(encoding="utf-8")

        set_up_py_samp()

        print("Start populate server entities")

        server_start()

        print("Population is finish successful")

    except Exception as ex:
        print("===================================================================\n"
              "        Something want wrong in server start up \n"
              "===================================================================\n")
        raise ex


@on_gamemode_exit
def server_exit():
    pass
