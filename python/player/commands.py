from pysamp import set_timer, kill_timer
from .inventory_functions import show_player_inventory
from .player import Player
from .timers import rout_create_handler
from ..job.rout import Rout
from ..permission.functions import check_permission
from ..utils.car import get_model_id_by_name
from ..utils.globals import MIN_VEHICLE_MODEL_ID, MAX_VEHICLE_MODEL_ID
from ..utils.player import is_valid_player
from ..utils.colors import Color
from pysamp.vehicle import Vehicle as BaseVehicle
from python.vehicle.vehicle import Vehicle
from ..utils.vars import VEHICLES


@Player.command(arg_names=None)
@Player.using_registry
def penztarca(player: Player):
    player.send_client_message(-1, f"((A pénztárcádban jelenleg {{00C0FF}} {player.money}Ft {{FFFFFF}}van.))")


@Player.command(aliases=("addpenz",), arg_names=['id/név', "összeg"])
@Player.using_registry
def givemoney(player: Player, target: str | int, value: float):
    target_player: Player | None = is_valid_player(target)

    if target_player is None:
        player.send_client_message(Color.WHITE, "(( Nincs ilyen játékos! ))")
        return

    target_player.money += value


@Player.command(arg_names=["model id / model name", "<color1>", "<color2>"])
@Player.using_registry
def newcar(player: Player, model_id: str | int, color1: int = 1, color2: int = 0):
    if model_id.isdigit() and (int(model_id) > MAX_VEHICLE_MODEL_ID or MIN_VEHICLE_MODEL_ID > int(model_id)):
        player.send_client_message(Color.RED, "(( Hiba: nincs ilyen model! ))")
        return

    if not model_id.isdigit():
        model_id = get_model_id_by_name(model_id)

    if model_id is None:
        player.send_client_message(Color.RED, "(( Hiba: Nincs ilyen típusú jármu! ))")
        return

    model_id = int(model_id)

    if model_id == 520 or model_id == 425 or model_id == 538 or model_id == 570 or model_id == 569 or model_id == 537:
        player.send_client_message(Color.RED, "(( Hiba: Ezt a jármuvet nem használhatod! ))")
        return

    (_, _, z) = player.get_pos()
    angle: float = player.get_facing_angle() + 90 if player.get_facing_angle() < 0 else player.get_facing_angle() - 90
    x, y = player.get_x_y_in_front_of_player(5)

    veh = BaseVehicle.create(model_id, x, y, z, angle, int(color1), int(color2), -1)
    veh.set_number_plate("NINCS")


@Player.command(arg_names=None)
@Player.using_registry
def taska(player: Player):
    show_player_inventory(player)


@Player.command(arg_names=None)
@Player.using_registry
def oldplayer(player: Player, vehicle_id: int = -1):
    vehicle: Vehicle | None = None

    if vehicle_id == -1:
        vehicle = player.get_vehicle()
    else:
        vehicle = VEHICLES[vehicle_id]

    if not vehicle:
        player.send_client_message(Color.RED, "(( Nincs ilyen jármű ))")
        return

    player.send_client_message(-1, "(( Kocsiban ült játéksok: ))")
    for row in vehicle.get_passenger_activity():
        player.send_client_message(-1, f"(( {row} ))")


@Player.using_registry
@Player.command(arg_names=None, requires=(check_permission('recordrout'), ))
def recordrout(player: Player, freq: int, r: float = 5):
    if player.is_recording:
        kill_timer(player.timers["recordrout"])
        player.send_client_message(Color.RED, "(( Utvonal rogzites befejezve ))")
        player.disable_checkpoint()
        return

    player.timers["recordrout"] = set_timer(rout_create_handler, int(freq) * 1000, True, player, r)

    player.send_client_message(Color.GREEN, f"(( Utvonal rogzites elkezdve. {freq} mp / checkpoint ))")

    (x, y, z) = player.get_pos()
    player.set_checkpoint(x, y, z, r)
    player.check_points.append(Rout(x, y, z, r))
    player.is_recording = True
