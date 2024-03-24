from pyeSelect.eselect import MenuItem
from python import exception_logger, PLAYER_COMMAND
from python.model.database import Role, CommandPermission
from python.model.server import Player, Vehicle
from python.server.database import MAIN_SESSION
from python.utils.enums.colors import Color
from python.utils.vars import ADMIN_PLAYERS, VEHICLES


@exception_logger.catch
@Player.using_registry
def check_player_role_permission(player: Player) -> bool | None:
    if player.role is None:
        return False

    cmd_txt: str = PLAYER_COMMAND[player.id]

    del PLAYER_COMMAND[player.id]

    with (MAIN_SESSION() as session):
        role: Role = session.query(Role).filter(Role.id == player.role.id).first()
        command_permission: CommandPermission = session.query(CommandPermission
                                                              ).filter(CommandPermission.cmd_txt == cmd_txt).first()

        if command_permission is None:
            return True

        if role is None:
            return False

        for role_permission in role.permissions:
            if role_permission.permission_type.id == command_permission.permission_type.id:
                return role_permission.power >= command_permission.need_power

        return False


@exception_logger.catch
@Player.using_registry
def send_admin_action(admin: Player, msg: str) -> None:
    send_msg = f'*ACMD* {admin.role.name} {admin.name} {msg}'

    with MAIN_SESSION() as session:
        sender = session.query(Role).get(admin.role.id)
        sender_power = next((e for e in sender.permissions if e.permission_type.code == 'admin_power'), None)

        for _, player in ADMIN_PLAYERS:
            notified = session.query(Role).get(player.role.id)
            notified_power = next((e for e in notified.permissions if e.permission_type.code == 'admin_power'), None)

            if notified_power.power >= sender_power.power:
                player.send_client_message(Color.LIGHT_RED, send_msg)


@exception_logger.catch
def send_acmd(msg: str, power: int = 0) -> None:
    send_msg = f'*ACMD* {msg}'

    with MAIN_SESSION() as session:
        for _, player in ADMIN_PLAYERS:
            notified = session.query(Role).get(player.role.id)
            notified_power = next((e for e in notified.permissions if e.permission_type.code == 'admin_power'), None)

            if notified_power.power >= power:
                player.send_client_message(Color.LIGHT_RED, send_msg)


@exception_logger.catch
@Player.using_registry
def spawn_admin_car(player: Player, menu_item: MenuItem):
    (_, _, z) = player.get_pos()
    angle: float = player.get_facing_angle() + 90 if player.get_facing_angle() < 0 else player.get_facing_angle() - 90
    x, y = player.get_x_y_in_front_of_player(5)

    color1, color2 = player.custom_vars["new_car_colors"]

    veh = Vehicle.create(menu_item.model_id, x, y, z, angle, int(color1), int(color2), -1)
    veh.set_number_plate("NINCS")
    VEHICLES[veh.id] = veh


@Player.using_registry
def change_skin(player: Player, menu_item: MenuItem):
    player.skin = menu_item.model_id
