from sqlalchemy import text

from pysamp import set_timer, kill_timer
from .inventory_functions import show_player_inventory
from .player import Player
from .timers import rout_create_handler
from ..eSelect.eselect import Menu, MenuItem
from ..fraction.fraction import Fraction
from ..job.rout import Rout
from ..permission.functions import check_permission
from ..server.database import MAIN_ENGINE
from ..teleports.teleport import Teleport
from ..utils.car import get_model_id_by_name
from ..utils.globals import MIN_VEHICLE_MODEL_ID, MAX_VEHICLE_MODEL_ID
from ..utils.player import is_valid_player
from ..utils.colors import Color
from pysamp.vehicle import Vehicle as BaseVehicle
from python.vehicle.vehicle import Vehicle
from ..utils.python_helpers import try_pars_int
from ..utils.vars import VEHICLES, LOGGED_IN_PLAYERS, SKINS, TELEPORTS, FRACTIONS


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
@Player.command(arg_names=None, requires=(check_permission('recordrout'),))
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


@Player.command
@Player.using_registry
def setskin(player: Player, target: str | int, value: int):
    target_player: Player | None = is_valid_player(target)

    if target_player is None:
        player.send_client_message(Color.RED, "(( Nincs ilyen játékos! ))")
        return

    c_value = try_pars_int(value)

    if c_value is None:
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")
        return

    if c_value == 74 or (0 > c_value > len(SKINS) - 1):
        player.send_client_message(Color.RED, "(( Nincs ilyen skin! ))")
        return

    if SKINS[c_value].sex != player.sex:
        player.send_client_message(Color.RED, f"(( Nem hathatsz {'noi' if SKINS[c_value].sex else 'fefi'} "
                                              f"skint egy {'no' if player.sex else 'fefi'}re! ))")
        return

    target_player.skin = int(c_value)


@Player.command
@Player.using_registry
def listskins(player: Player):
    menu = Menu(
        'Ruhák',
        [MenuItem(skin.id, str(skin.price) + " Ft") for skin in SKINS if skin.sex == player.sex and skin.id != 74],
        on_select=change_skin,
    )

    menu.show(player)


@Player.using_registry
def change_skin(player: Player, menu_item: MenuItem):
    player.skin = menu_item.model_id


@Player.command
@Player.using_registry
def gotopos(player: Player, x: float, y: float, z: float, interior=0, vw=0):
    player.set_pos(float(x), float(y), float(z))
    player.set_interior(int(interior))
    player.set_virtual_world(int(vw))


@Player.command
@Player.using_registry
def getpos(player: Player):
    x, y, z = player.get_pos()
    a = player.get_facing_angle()

    player.send_client_message(Color.WHITE, f"(( X >> {x: .4f} | Y >> {y: .4f} | Z >> {z: .4f} | A >> {a: .4f} ))")


@Player.using_registry
@Player.command(aliases=("duty",))
def szolg(player: Player):
    if not player.fraction:
        player.send_client_message(Color.RED, "(( Nem vagy egy frakció tagja se! ))")
        return

    if not player.in_duty_point:
        player.send_client_message(Color.RED, "(( Nem vagy a megfelelo helyen! ))")
        return

    if player.in_duty:
        player.in_duty = False
        player.send_client_message(Color.GREEN, "(( Kiléptél a szolgálatból ))")
        player.set_skin(player.skin.id)
        return

    if not player.fraction_skin:
        player.send_client_message(Color.RED, "(( Nem megfelelo a szolgalati ruhad! Valasz egyet! ))")

        menu = Menu(
            'Frakcio ruhak',
            [MenuItem(skin.id) for skin in player.fraction.skins if skin.sex == player.sex],
            on_select=change_fk_skin,
        )

        menu.show(player)
        return

    player.in_duty = True
    player.send_client_message(Color.GREEN, "(( Szolgalata alltal! ))")
    player.set_skin(player.fraction_skin.id)


@Player.using_registry
def change_fk_skin(player: Player, menu_item: MenuItem):
    player.send_client_message(Color.GREEN, "(( Sikeresen választottál ruhát! Allj szolgalatba! ))")
    player.fraction_skin = menu_item.model_id


@Player.using_registry
@Player.command
def savedutypoint(player: Player, fraction_id: int, size: float = 3.0):
    (x, y, z) = player.get_pos()
    interior = player.get_interior()
    vw = player.get_virtual_world()

    mapper = {
        'fraction_id': int(fraction_id),
        'x': x,
        'y': y,
        'z': z,
        'size': float(size),
        'interior': interior,
        'virtual_word': vw
    }

    with MAIN_ENGINE.connect() as conn:
        query: text = text(
            "INSERT INTO fraction_duty_locations("
            "fraction_id, x, y, z, size, interior, virtual_word) "
            "VALUES (:fraction_id, :x, :y, :z, :size, :interior, :virtual_word);")
        conn.execute(query, mapper)
        conn.commit()

    fk: Fraction = FRACTIONS[int(fraction_id)]
    fk.load_duty_location()
