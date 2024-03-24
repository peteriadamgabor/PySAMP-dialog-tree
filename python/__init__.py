import samp


samp.config(encoding='cp1250')

from pysamp.player import Player
from pysamp.commands import dispatcher as main_dispatcher

from datetime import datetime
from time import perf_counter

from pysamp import on_gamemode_init

from .logging import sqlalchemy
from .logging.loggers import exception_logger, debugger, command_logger

from .utils.vars import PLAYER_COMMAND

from .model import database
from .server import database
from . import zone
from . import events
from . import command
from . import utils
from . import player
from . import business
from . import house
from . import vehicle
from . import admin

from .server.functions import server_start, set_up_py_samp


@exception_logger.catch
@on_gamemode_init
def server_init():

    start_time: float = perf_counter()
    debugger.info(f"Server starting at: {datetime.now()}")

    set_up_py_samp()

    server_start()

    debugger.info(f"Server starting finished at: {datetime.now()}")
    end_time: float = perf_counter()
    debugger.info(f"It took {end_time - start_time:.3f} seconds")


def OnPlayerCommandText(playerid: int, cmdtext: str):

    cmd_player = Player(playerid)
    log_str: str = f"{cmdtext} - {cmd_player.get_name()}"
    command_logger.info(log_str)

    PLAYER_COMMAND[playerid] = cmdtext.split(" ")[0][1:]

    if not main_dispatcher.handle(playerid, cmdtext):
        Player(playerid).send_client_message(-1, "(( Ismertelen parancs! ))")
    return True
