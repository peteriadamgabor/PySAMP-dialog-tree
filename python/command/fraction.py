from pyeSelect.eselect import MenuItem, Menu

from python.model.server import Player
from python.utils.enums.colors import Color
from python.utils.helpers import list_skins


@Player.using_registry
def change_fk_skin(player: Player, menu_item: MenuItem):
    player.send_client_message(Color.GREEN, "(( Sikeresen választottál ruhát! Allj szolgalatba! ))")
    player.fraction_skin = menu_item.model_id


@Player.using_registry
@Player.command(aliases=("duty",))
def szolg(player: Player):
    if player.fraction is None:
        player.send_client_message(Color.RED, "(( Nem vagy egy frakció tagja se! ))")
        return

    if not player.in_duty_point and player.fraction is not None and int(player.fraction.duty_everywhere) == 0:
        player.send_client_message(Color.RED, "(( Nem vagy a megfelelo helyen! ))")
        return

    if player.in_duty:
        player.in_duty = False
        player.send_client_message(Color.GREEN, "(( Kiléptél a szolgálatból ))")
        player.set_skin(player.skin.id)
        player.reset_weapons()
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
    player.reset_weapons()
    player.give_weapon(3, 1)
    player.give_weapon(41, 200)
    player.give_weapon(24, 21)
    return
