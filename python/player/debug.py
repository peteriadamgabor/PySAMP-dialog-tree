from python.dialogtree.dialogtree import DialogTreeNode, DialogTree
from python.model.database import PlayerModel
from python.model.server import Player
from python.server.database import MAIN_SESSION, PLAYER_SESSION
from python.utils.enums.dialog_style import DialogStyle


@Player.command
@Player.using_registry
def debug(player: Player):
    root_dialog = DialogTreeNode("root", DialogStyle.LIST, "Admin control panel",
                                 "User management\nServer settings",
                                 "Ok", "Close")

    with MAIN_SESSION() as session:
        players = session.query(PlayerModel).all()

        u_content = '\n'.join(
            [f"DBID: #dbid->{m_player.id}# | Name: {m_player.name}" for m_player in players])

        user_management = DialogTreeNode("user_management", DialogStyle.LIST, "User management",
                                         u_content, "Select", "Back")

        user_data = DialogTreeNode("user_data", DialogStyle.LIST, "User data management",
                                   "", "Select", "Back",
                                   custom_content_handler=user_data_context_handler,
                                   stay_if_none=True,
                                   custom_content_handler_node_parameters=("user_management.dbid",),
                                   )

        user_money_editor = DialogTreeNode("user_money_editor", DialogStyle.INPUT,
                                           "User data management - Money editor",
                                           f"Enter the user new money. Current: #user_data.money# Ft",
                                           "Save", "Back",
                                           back_after_save=True,
                                           custom_handler=user_data_money_handler,
                                           custom_handler_node_parameters=("user_management.dbid",))

    dialog_tree = DialogTree(root_dialog)
    root_dialog.add_child(user_management)

    user_management.add_child(user_data)
    user_data.add_child(None)
    user_data.add_child(None)
    user_data.add_child(user_money_editor)

    dialog_tree.show_root_dialog(player)


@Player.using_registry
def user_data_money_handler(player: Player, response: int, list_item: int, input_text: str, *args, **kwargs):

    with PLAYER_SESSION() as session:
        player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == int(args[0])).first()
        player_model.money = float(input_text)
        session.commit()

    player.send_client_message(-1, "Successfully updated")


def user_data_context_handler(dbid: str) -> str:

    with MAIN_SESSION() as session:
        player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == int(dbid)).first()

        return f"DBID: {dbid} \nName: {player_model.name} \nMoney: #money->{player_model.money}# Ft \nRole: {player_model.role.name}"
