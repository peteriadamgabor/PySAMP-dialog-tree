from sqlalchemy import and_

from python.model.database import PlayerModel, Item, InventoryItem
from python.model.server import Player
from python.server.database import PLAYER_SESSION
from python.utils.enums.colors import Color
from python.utils.enums.itemtypes import ItemType
from python.utils.player import get_player, get_nearest_player


@Player.using_registry
def list_player_inventory(player: Player, is_search: bool = False) -> str:
    with PLAYER_SESSION() as session:
        player_model: PlayerModel = session.query(PlayerModel).filter(PlayerModel.id == player.dbid).first()

        ret = ""

        for inventory_item in player_model.items:

            metad_data = ""

            if inventory_item.inventory_item_data.vehicle and not is_search:
                metad_data = inventory_item.inventory_item_data.vehicle.plate
                ret += (f"\n#dbid~>{inventory_item.id}##amount->{inventory_item.amount}#"
                        f"\t#name->{inventory_item.item.name}#"
                        f"\t{metad_data}")
            else:
                ret += (f"\n#dbid~>{inventory_item.id}##amount->{inventory_item.amount}#"
                        f"\t#name->{inventory_item.item.name}#"
                        f"\t{metad_data}")

        return ret


@Player.using_registry
def handel_item_use(player: Player, _, __, ___, *args, ____) -> None:
    with PLAYER_SESSION() as session:
        pii: InventoryItem = session.query(InventoryItem).filter(InventoryItem.id == args[0]).first()

        item: Item = pii.item

        if not item or not pii:
            return None

        match item.data.type:
            case ItemType.FOOD:
                player.set_health(player.get_health() + item.data.heal)
                return None

            case ItemType.WEAPON:
                player.give_weapon(item.data.weapon_id, pii.amount)
                return None

            case _:
                return None


@Player.using_registry
def check_is_split_item(_: Player, *args) -> bool:
    with PLAYER_SESSION() as session:
        pii: InventoryItem = session.query(InventoryItem).filter(InventoryItem.id == args[0]).first()
        return pii.item.is_stackable


@Player.using_registry
def handel_direct_transfer_item(player: Player, _, __, input_text: str, *args) -> None:
    target_player: Player | None = get_player(input_text) if input_text != '-1' else get_nearest_player(player)

    if target_player is None:
        if input_text != '-1':
            player.send_system_message(Color.ORANGE, "(( Nincs ilyen játékos!))")
        else:
            player.send_system_message(Color.ORANGE, "(( Nincs senki a közeledben!))")
        return

    with PLAYER_SESSION() as session:
        pii: InventoryItem = session.query(InventoryItem).filter(InventoryItem.id == args[0]).first()
        pii.player_id = target_player.dbid
        session.commit()


@Player.using_registry
def handel_indirect_transfer_item(player: Player, _, __, input_text: str, *args) -> None:
    target_player: Player | None = get_player(args[0]) if args[0] != '-1' else get_nearest_player(player)

    if target_player is None:
        if input_text != '-1':
            player.send_system_message(Color.ORANGE, "Nincs ilyen játékos!")
        else:
            player.send_system_message(Color.ORANGE, "Nincs senki a közeledben!")
        return

    inventory_item_id = int(args[1])
    transfer_amount = int(args[2])

    if player.have_enough_item(inventory_item_id):
        player.send_system_message(Color.RED, "Nincs nálad ennyi!")
        return

    player.transfer_item(target_player, inventory_item_id, transfer_amount)


@Player.using_registry
def handel_item_drop(player: Player, response: int, list_item: int, input_text: str):
    if not bool(response):
        return

    if not input_text.isdigit():
        player.send_client_message(Color.RED, "(( Számmal kell megadni! ))")

    amount = int(input_text)

    if amount <= 0:
        player.send_client_message(Color.RED, "(( Érvénytelen mennyiség! ))")

    item: InventoryItem = player.items[list_item]

    new_amount = item.amount - amount

    if new_amount == 0:
        player.dialog_vars["selected_item"] = None

    else:
        item.amount = new_amount
