from datetime import datetime
from sqlalchemy import text

from .inventory_functions import show_player_inventory
from python.model.server import Player, Vehicle
from pyeSelect.eselect import Menu, MenuItem
from ..model.database import Skin
from ..server.database import MAIN_ENGINE, MAIN_SESSION
from ..server.functions import load_teleports
from ..utils.car import get_model_id_by_name
from ..utils.enums.colors import Color
from ..utils.globals import MIN_VEHICLE_MODEL_ID, MAX_VEHICLE_MODEL_ID
from ..utils.player import is_valid_player, get_nearest_gate
from ..utils.python_helpers import try_pars_int, format_numbers
from ..utils.vars import VEHICLES, LOGGED_IN_PLAYERS, SKINS, FRACTIONS


@Player.command
@Player.using_registry
def penztarca(player: Player):
    player.send_client_message(-1,
                               f"((A pénztárcádban jelenleg {{00C0FF}} {format_numbers(int(player.money))}Ft {{FFFFFF}}van.))")


@Player.command
@Player.using_registry
def ido(player: Player):
    player.send_client_message(-1, f"((A pontos idő: {{00C0FF}} {datetime.now():%Y.%m.%d %X} {{FFFFFF}}))")


@Player.command
@Player.using_registry
def taska(player: Player):
    show_player_inventory(player)


@Player.using_registry
@Player.command
def adminok(player: Player):
    player.send_client_message(Color.WHITE, "(( Online adminok: ))")

    for lplayer in LOGGED_IN_PLAYERS:

        if lplayer is None or lplayer.role is None:
            continue

        if lplayer.role:
            player.send_client_message(Color.WHITE, f"(({{F81414}}{lplayer.name}{{FFFFFF}} | Szint:"
                                                    f"{{F81414}} {lplayer.role.name} {{FFFFFF}}))")



@Player.using_registry
@Player.command
def nyit(player: Player):
    (x, y, z) = player.get_pos()
    interior = player.get_interior()
    vw = player.get_virtual_world()

    gate = get_nearest_gate((x, y, z))

    if gate:
        gate.open()

        if gate.auto:
            player.send_client_message(Color.WHITE, f"(( A kapu / ajtó {gate.close_time} másodperc múlva záródik! ))")
        else:
            player.send_client_message(Color.WHITE, f"(( Ez a kapu / ajtó manuális, nem záródik autómatikusan! ))")

    else:
        player.send_client_message(Color.RED, "(( Nincs a közelben ajtó / kapu amit ki tudnál nyitni! ))")


@Player.using_registry
@Player.command
def zar(player: Player):
    (x, y, z) = player.get_pos()
    interior = player.get_interior()
    vw = player.get_virtual_world()

    gate = get_nearest_gate((x, y, z))

    if gate:
        gate.close()

    else:
        player.send_client_message(Color.RED, "(( Nincs a közelben ajtó / kapu amit be tudnál zárni! ))")


@Player.using_registry
@Player.command
def torol(player: Player):
    player.disable_checkpoint()

