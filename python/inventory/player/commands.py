from python.dialogtree.dialogtree import DialogTree, DialogTreeNode
from python.inventory.player.functions import list_player_inventory, handel_item_use, handel_direct_transfer_item, \
    check_is_split_item, handel_indirect_transfer_item
from python.model.server import Player
from python.utils.enums.colors import Color
from python.utils.enums.dialog_style import DialogStyle


@Player.command
@Player.using_registry
def taska(player: Player):
    if not player.items:
        player.send_client_message(Color.ORANGE, "(( Üres a táskád! ))")
        return

    root_node: DialogTreeNode = DialogTreeNode("inventory_root", DialogStyle.TABLIST_HEADERS, "Táska",
                                               "Mennyiség\tNév\tAdat\n", "Kiválaszt", "Bezár",
                                               custom_content_handler=list_player_inventory)

    item_node: DialogTreeNode = DialogTreeNode("inventory_item", DialogStyle.LIST, "#inventory_root.name#",
                                               "Haszán\nÁtad\nEldob", "Kiválaszt", "Vissza")

    use_node: DialogTreeNode = DialogTreeNode("inventory_use", DialogStyle.LIST, "",
                                              "", "", "",
                                              just_action=True,
                                              back_after_input=True,
                                              custom_handler=handel_item_use,
                                              custom_handler_parameters=("inventory_root.dbid",))

    transfer_p_node: DialogTreeNode = DialogTreeNode("inventory_transfer_p", DialogStyle.LIST, "Táska - átadás",
                                                     "Add meg a játékos nevét/id -jét akinek adni akarod."
                                                     "\nHa a hozzád legközelebbi játékosnak akarod adni, írj '-1' -et!",
                                                     "Átad", "Mégsem",
                                                     is_guarded_handler=True,
                                                     save_input=True,
                                                     guard=check_is_split_item,
                                                     guard_node_parameters=("inventory_root.dbid",),
                                                     custom_handler=handel_direct_transfer_item,
                                                     custom_handler_parameters=("inventory_root.dbid",))

    transfer_a_node: DialogTreeNode = DialogTreeNode("inventory_transfer_a", DialogStyle.LIST, "Táska - átadás",
                                                     "Add meg a mennyiséget!"
                                                     "\nTárgy: #inventory_root.name# mennyiség:#inventory_root.amount#",
                                                     "Átad", "Mégsem",
                                                     is_guarded_handler=True,
                                                     save_input=True,
                                                     guard=check_is_split_item,
                                                     guard_node_parameters=("inventory_root.dbid",),
                                                     custom_handler=handel_indirect_transfer_item,
                                                     custom_handler_parameters=("inventory_root.dbid",))

    item_node.add_child(use_node)
    item_node.add_child(transfer_p_node)
    transfer_p_node.add_child(transfer_a_node)
    root_node.add_child(item_node)

    inventory_root: DialogTree = DialogTree()
    inventory_root.add_root(root_node)
    inventory_root.show_root_dialog(player)
