from python.command.command import cmd
from .player import Player
from ..utils.car import get_model_id_by_name
from ..utils.globals import MIN_VEHICLE_ID, MAX_VEHICLE_ID
from ..utils.player import is_valid_player
from ..utils.colors import Color
from pysamp.vehicle import Vehicle


@cmd
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

    target_player.money = value


@Player.command(custom_usage_message="Használat: /newcar [modelid/modelname] <color1> <color2>")
@Player.using_registry
def newcar(player: Player, model_id: str | int, color1: int = 1, color2: int = 0):
    if model_id.isdigit() and (int(model_id) > MAX_VEHICLE_ID or MIN_VEHICLE_ID > int(model_id)):
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

    veh = Vehicle.create(model_id, x, y, z, angle, int(color1), int(color2), -1)
    veh.set_number_plate("NINCS")
