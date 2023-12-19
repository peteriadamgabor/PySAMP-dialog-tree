from pysamp.dialog import Dialog
from python.items.item_types import ItemType
from python.items.playerinventoryitem import PlayerInventoryItem
from python.player.player import Player
from python.utils.colors import Color
from python.utils.dialog_style import DialogStyle


@Player.using_registry
def show_player_inventory(player: Player):
    player.dialog_vars["selected_item"] = None

    if not player.inventory.items:
        player.send_client_message(Color.ORANGE, "(( Üres a táskád! ))")
        return

    content = "Mennyiség\tNév\tAdat\n"
    content += '\n'.join([f"{item.amount}\t{item.name}\t{''}"
                          for item in player.inventory.items])

    player.show_dialog(Dialog.create(5, "Táska", content, "Ok", "Mégsem",
                                     on_response=handel_inventory_select))


@Player.using_registry
def handel_inventory_select(player: Player, response: int, list_item: int, input_text: str):
    if not bool(response):
        return

    item: PlayerInventoryItem = player.inventory.items[list_item]

    player.dialog_vars["selected_item"] = item

    player.show_dialog(Dialog.create(DialogStyle.LIST, "Táska", "Haszán\nÁtad\nEldob",
                                     "Ok", "Mégsem", on_response=handel_item_select))


@Player.using_registry
def handel_item_select(player: Player, response: int, list_item: int, input_text: str):
    if not bool(response):
        show_player_inventory(player)
        return

    item: PlayerInventoryItem = player.dialog_vars.get("selected_item", None)

    if not item:
        return

    match list_item:
        case 0:
            handel_item_use(player, item)

        case 1:
            if item.droppable:
                if item.is_stackable and item.amount > 1:
                    player.show_dialog(Dialog.create(DialogStyle.INPUT, "Eldobás", "Add meg mennyit szeretnél eldobni", "Mehet", "Mégsem", on_response=handel_item_drop))
                else:
                    player.dialog_vars["selected_item"] = None

        case _:
            show_player_inventory(player)


@Player.using_registry
def handel_item_use(player: Player, item: PlayerInventoryItem):

    if not item.data:
        return

    match item.data.type:
        case ItemType.FOOD:
            player.set_health(player.get_health() + item.data.heal)

        case ItemType.WEAPON:
            player.give_weapon(item.data.weapon_id, item.amount)

    player.dialog_vars["selected_item"] = None


@Player.using_registry
def handel_item_drop(player: Player, response: int, list_item: int, input_text: str):

    if not bool(response):
        return

    if not input_text.isdigit():
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")

    amount = int(input_text)

    if amount <= 0:
        player.send_client_message(Color.RED, "(( Érvénytelen mennyiség! ))")

    item: PlayerInventoryItem = player.inventory.items[list_item]

    new_amount = item.amount - amount

    if new_amount == 0:
        player.dialog_vars["selected_item"] = None

    else:
        item.amount = new_amount
