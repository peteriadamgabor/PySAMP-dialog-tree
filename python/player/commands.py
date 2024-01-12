from sqlalchemy import text

from .events import handle_engine_switch
from .inventory_functions import show_player_inventory
from python.model.server import Player, Vehicle
from python.utils.enums.states import State
from pyeSelect.eselect import Menu, MenuItem
from ..server.database import MAIN_ENGINE
from ..server.functions import load_teleports
from ..utils.car import get_model_id_by_name
from ..utils.enums.colors import Color
from ..utils.globals import MIN_VEHICLE_MODEL_ID, MAX_VEHICLE_MODEL_ID
from ..utils.player import is_valid_player, get_nearest_gate
from ..utils.python_helpers import try_pars_int
from ..utils.vars import VEHICLES, LOGGED_IN_PLAYERS, SKINS, FRACTIONS


@Player.command
@Player.using_registry
def penztarca(player: Player):
    player.send_client_message(-1, f"((A pénztárcádban jelenleg {{00C0FF}} {player.money}Ft {{FFFFFF}}van.))")


@Player.command
@Player.using_registry
def givemoney(player: Player, target: str | int, value: float):
    target_player: Player | None = is_valid_player(target)

    if target_player is None:
        player.send_client_message(Color.WHITE, "(( Nincs ilyen játékos! ))")
        return

    target_player.money += float(value)


@Player.command
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

    veh = Vehicle.create(model_id, x, y, z, angle, int(color1), int(color2), -1)
    veh.set_number_plate("NINCS")
    VEHICLES[veh.id] = veh


@Player.command
@Player.using_registry
def newcarl(player: Player, color1: int = 1, color2: int = 0):
    forbidden = [520, 425, 538, 570, 569, 537]

    player.custom_vars["new_car_colors"] = (int(color1), int(color2))

    menu = Menu(
        'Autók',
        [MenuItem(i, '', -15.0, 0.0, -45.0, 1, int(color1), int(color2)) for i in range(400, 612) if
         i not in forbidden],
        on_select=spawn_admin_car,
    )

    menu.show(player)


@Player.using_registry
def spawn_admin_car(player: Player, menu_item: MenuItem):
    (_, _, z) = player.get_pos()
    angle: float = player.get_facing_angle() + 90 if player.get_facing_angle() < 0 else player.get_facing_angle() - 90
    x, y = player.get_x_y_in_front_of_player(5)

    color1, color2 = player.custom_vars["new_car_colors"]

    veh = Vehicle.create(menu_item.model_id, x, y, z, angle, int(color1), int(color2), -1)
    veh.set_number_plate("NINCS")
    VEHICLES[veh.id] = veh


@Player.command
@Player.using_registry
def taska(player: Player):
    show_player_inventory(player)


@Player.command
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
    pos: tuple[float, float, float] = player.get_pos()
    p_interior: int = player.get_interior()
    p_vw: int = player.get_virtual_world()
    p_a: float = player.get_facing_angle()

    player.custom_vars["back_pos"] = (pos, p_interior, p_vw, p_a)
    player.set_pos(float(x), float(y), float(z))
    player.set_interior(int(interior))
    player.set_virtual_world(int(vw))


@Player.command
@Player.using_registry
def back(player: Player):
    if player.custom_vars["back_pos"]:
        (x, y, z) = player.custom_vars["back_pos"][0]
        interior: int = player.custom_vars["back_pos"][1]
        vw: int = player.custom_vars["back_pos"][2]
        a: float = player.custom_vars["back_pos"][3]

        player.set_pos(float(x), float(y), float(z))
        player.set_interior(int(interior))
        player.set_virtual_world(int(vw))
        player.set_facing_angle(a)


@Player.command
@Player.using_registry
def getpos(player: Player):
    x, y, z = player.get_pos()
    a = player.get_facing_angle()

    player.send_client_message(Color.WHITE, f"(( X >> {x: .4f} | Y >> {y: .4f} | Z >> {z: .4f} | A >> {a: .4f} ))")


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
def createteleport(player: Player, radius: float, description: str):
    pos: tuple[float, float, float] = player.get_pos()
    interior: int = player.get_interior()
    vw: int = player.get_virtual_world()
    a: float = player.get_facing_angle()

    if "teleport_data" not in player.custom_vars:
        player.custom_vars["teleport_data"] = (pos, interior, vw, a, radius, description)
        player.send_client_message(Color.GREEN, "(( Sikersenen mentetted a pontot! Menny a következohöz! ))")
        return

    else:
        data = player.custom_vars["teleport_data"]

        del player.custom_vars["teleport_data"]

        mapper_from = {
            'from_x': data[0][0],
            'from_y': data[0][1],
            'from_z': data[0][2],
            'from_interior': data[1],
            'from_vw': data[2],
            'radius': data[4],
            'to_x': pos[0],
            'to_y': pos[1],
            'to_z': pos[2],
            'to_angel': a,
            'to_interior': interior,
            'to_vw': vw,
            'description': data[5],
        }

        mapper_to = {
            'from_x': pos[0],
            'from_y': pos[1],
            'from_z': pos[2],
            'from_interior': interior,
            'from_vw': vw,
            'radius': radius,
            'to_x': data[0][0],
            'to_y': data[0][1],
            'to_z': data[0][2],
            'to_angel': data[3],
            'to_interior': data[1],
            'to_vw': data[2],
            'description': description,
        }

        with MAIN_ENGINE.connect() as conn:
            query: text = text(
                "INSERT INTO zone("
                "from_x, from_y, from_z, from_interior, from_vw, radius, "
                "to_x, to_y, to_z, to_angel, to_interior, to_vw, description)"
                " VALUES (:from_x, :from_y, :from_z, :from_interior, :from_vw, :radius,"
                " :to_x, :to_y, :to_z, :to_angel, :to_interior, :to_vw, :description);")
            conn.execute(query, mapper_from)
            conn.execute(query, mapper_to)
            conn.commit()

        player.send_client_message(Color.GREEN, "(( Sikersenen elmentetted a teleportot! Tölsd újra! ))")


@Player.using_registry
@Player.command
def reloadteleports(player: Player):
    load_teleports()
    player.send_client_message(Color.LIGHT_RED, "(( Sikeresen újratöltötted a teleportokat! ))")


@Player.using_registry
@Player.command
def kor(player: Player, r: float):
    x, y, z = player.get_pos()
    player.set_checkpoint(x, y, z, float(r))


@Player.using_registry
@Player.command
def torol(player: Player):
    player.disable_checkpoint()


@Player.using_registry
@Player.command
def indit(player: Player):
    if player.get_state() != State.DRIVER:
        player.send_client_message(Color.RED, "(( Nem vagy sofor! ))")
        return

    vehicle: Vehicle = player.get_vehicle()
    handle_engine_switch(player, vehicle)


@Player.using_registry
@Player.command
def leallit(player: Player):
    if player.get_state() != State.DRIVER:
        player.send_client_message(Color.RED, "(( Nem vagy sofor! ))")
        return

    vehicle: Vehicle = player.get_vehicle()
    vehicle.engine = 0


@Player.using_registry
@Player.command
def fixveh(player: Player):

    vehicle: Vehicle = player.get_vehicle()

    if vehicle:
        vehicle.skip_check_damage = True
        vehicle.health = 1_000
        vehicle.repair()


@Player.using_registry
@Player.command
def setvehhp(player: Player, health: float):

    vehicle: Vehicle = player.get_vehicle()

    if vehicle:
        vehicle.skip_check_damage = True
        vehicle.health = health
