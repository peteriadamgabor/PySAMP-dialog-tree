from python.model.server import Player, Vehicle
from python.utils.enums.colors import Color
from python.utils.enums.states import State
from python.vehicle.functions import handle_engine_switch


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

