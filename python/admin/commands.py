from python.model.server import Player, Vehicle
from pyeSelect.eselect import Menu, MenuItem
from ..utils.item import is_valid_item_id
from .functions import check_player_role_permission, send_admin_action, spawn_admin_car, change_skin
from .. import exception_logger
from ..model.database import Skin
from ..server.database import MAIN_SESSION
from ..utils.car import get_model_id_by_name
from ..utils.enums.colors import Color
from ..utils.enums.states import State
from ..utils.globals import MIN_VEHICLE_MODEL_ID, MAX_VEHICLE_MODEL_ID
from ..utils.player import get_player
from ..utils.python_helpers import try_pars_int, format_numbers
from ..utils.vars import VEHICLES, SKINS


@Player.command(args_name=("id/név", "összeg"), requires=[check_player_role_permission])
@Player.using_registry
def givemoney(player: Player, target: str | int, value: float, *args):
    target_player: Player | None = get_player(target)

    if target_player is None:
        player.send_client_message(Color.WHITE, "(( Nincs ilyen játékos! ))")
        return

    target_player.money += float(value)

    send_admin_action(player, f"{format_numbers(value)} Ft-ot adott {target_player.name}")


@Player.command(args_name=("id/név",), requires=[check_player_role_permission])
@Player.using_registry
def goto(player: Player, target: str | int, seat: int = 1):
    target_player: Player | None = get_player(target)

    if target_player is None:
        player.send_client_message(Color.WHITE, "(( Nincs ilyen játékos! ))")
        return

    player.interior = target_player.interior
    player.virtual_world = target_player.virtual_world

    (x, y) = target_player.get_x_y_in_front_of_player(2)
    (_, _, z) = target_player.get_pos()
    angle = target_player.get_facing_angle()

    if player.in_vehicle() and player.get_state() == State.DRIVER:
        veh: Vehicle = player.get_vehicle()

        veh.set_position(x, y, z + 2)
        player.send_client_message(Color.GREEN,
                                   f"(( {target_player.name}[{target_player.id}]-hez lettél teleportálva! ))")
        return

    elif target_player.in_vehicle():
        player.put_in_vehicle(target_player.get_vehicle_id(), seat)
        player.send_client_message(Color.GREEN,
                                   f"(( {target_player.name}[{target_player.id}] járművébe lettél teleportálva! ))")
        return

    else:
        if angle < 0.0:
            angle = angle + 180.0

        if angle > 0.0:
            angle = angle - 180.0

        player.set_pos(x, y, z)
        player.set_facing_angle(angle)
        player.send_client_message(Color.GREEN,
                                   f"(( {target_player.name}[{target_player.id}]-hez lettél teleportálva! ))")
        return


@Player.command(args_name=("id/név",), requires=[check_player_role_permission])
@Player.using_registry
def gethere(player: Player, target: str | int, seat: int = 1):
    target_player: Player | None = get_player(target)

    if target_player is None:
        player.send_client_message(Color.WHITE, "(( Nincs ilyen játékos! ))")
        return

    target_player.interior = player.interior
    target_player.virtual_world = player.virtual_world

    (x, y) = player.get_x_y_in_front_of_player(2)
    (_, _, z) = player.get_pos()
    angle = player.get_facing_angle()

    if player.in_vehicle() and player.get_state() == State.DRIVER:
        target_player.put_in_vehicle(player.get_vehicle_id(), seat)
        player.send_client_message(Color.GREEN,
                                   f"(( {target_player.name}[{target_player.id}] járművedbe lett teleportálva! ))")
        target_player.send_client_message(Color.GREEN, f"(( Teleportálva lettél! ))")
        return

    elif target_player.in_vehicle():
        veh: Vehicle = target_player.get_vehicle()

        veh.set_position(x, y, z + 2)
        player.send_client_message(Color.GREEN,
                                   f"(( {target_player.name}[{target_player.id}] járműve teleportálva lett! ))")
        target_player.send_client_message(Color.GREEN, f"(( Teleportálva lettél! ))")
        return

    else:
        if angle < 0.0:
            angle = angle + 180.0

        if angle > 0.0:
            angle = angle - 180.0

        target_player.set_pos(x, y, z)
        target_player.set_facing_angle(angle)

        target_player.send_client_message(Color.GREEN, f"(( Teleportálva lettél! ))")
        player.send_client_message(Color.GREEN,
                                   f"(( {target_player.name}[{target_player.id}]-hez lettél teleportálva! ))")
        return


@Player.command(args_name=("modelid/modelname", "color1", "color2"), requires=[check_player_role_permission])
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


@Player.command(requires=[check_player_role_permission])
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


@Player.command(args_name=("Kocsi DBID",), requires=[check_player_role_permission])
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


@Player.command(args_name=("id/név", "skinid"), requires=[check_player_role_permission])
@Player.using_registry
def setskin(player: Player, target: str | int, value: int):
    target_player: Player | None = get_player(target)

    if target_player is None:
        player.send_client_message(Color.RED, "(( Nincs ilyen játékos! ))")
        return

    c_value = try_pars_int(value)

    if c_value is None:
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")
        return

    with MAIN_SESSION() as session:
        skin: Skin = session.query(Skin).filter(Skin.id == c_value).first()

        if skin is None:
            player.send_client_message(Color.RED, "(( Nincs ilyen skin! ))")
            return

        if skin.sex != player.sex:
            player.send_client_message(Color.RED, f"(( Nem hathatsz {'noi' if SKINS[c_value].sex else 'fefi'} "
                                                  f"skint egy {'no' if player.sex else 'fefi'}re! ))")
            return

        target_player.skin = int(c_value)


@Player.command(requires=[check_player_role_permission])
@Player.using_registry
def listskins(player: Player):
    with MAIN_SESSION() as session:
        skins = session.query(Skin).order_by(Skin.id).all()
        menu = Menu(
            'Ruhák',
            [MenuItem(skin.id, str(skin.price) + " Ft") for skin in skins if skin.sex == player.sex and skin.id != 74],
            on_select=change_skin,
        )
        menu.show(player)


@Player.command(requires=[check_player_role_permission])
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


@Player.command(requires=[check_player_role_permission])
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


@Player.command(requires=[check_player_role_permission])
@Player.using_registry
def getpos(player: Player):
    x, y, z = player.get_pos()
    a = player.get_facing_angle()

    player.send_client_message(Color.WHITE, f"(( X >> {x: .4f} | Y >> {y: .4f} | Z >> {z: .4f} | A >> {a: .4f} ))")


@Player.command(requires=[check_player_role_permission])
@Player.using_registry
def fixveh(player: Player):
    vehicle: Vehicle = player.get_vehicle()

    if vehicle:
        vehicle.skip_check_damage = True
        vehicle.health = 1_000
        vehicle.repair()


@Player.command(requires=[check_player_role_permission])
@Player.using_registry
def setvehhp(player: Player, health: float):
    vehicle: Vehicle = player.get_vehicle()

    if vehicle:
        vehicle.skip_check_damage = True
        vehicle.health = health


@Player.command(args_name=("id/név",), requires=[check_player_role_permission])
@Player.using_registry
def asegit(player: Player, target: str | int):
    target_player: Player | None = get_player(target)

    if target_player is None:
        player.send_client_message(Color.WHITE, "(( Nincs ilyen játékos! ))")
        return

    target_player.set_drunk_level(0)
    target_player.apply_animation("PED", "getup_front", 4.0, False, False, False, False, 0, True)
    player.send_client_message(Color.GREEN, "(( Játékos sikeresen felsegítve! ))")
    target_player.send_client_message(Color.GREEN, "(( Egy admin felsegített! ))")


@Player.command(args_name=("id/név", "item id", "mennyiség"), requires=[check_player_role_permission])
@Player.using_registry
@exception_logger.catch
def giveitem(player: Player, target: str | int, item_id: int, amount: int, *args):
    target_player: Player | None = get_player(target)
    item_id = int(item_id)

    if target_player is None:
        player.send_system_message(Color.RED, "Nincs ilyen játékos!")
        return

    if not is_valid_item_id(item_id):
        player.send_system_message(Color.RED, "Nincs ilyen item!")
        return

    if (transfer_amount := try_pars_int(amount)) is None:
        player.send_system_message(Color.RED, "Számmal kell megadni!")
        return

    if transfer_amount < 0:
        player.send_system_message(Color.RED, "Negatív szám nem lehet!")
        return

    target_player.give_item(item_id, transfer_amount)
