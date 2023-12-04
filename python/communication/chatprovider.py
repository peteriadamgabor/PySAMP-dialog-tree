from ..utils import LOGGED_IN_PLAYERS, Color


def send_public_kick_message(message: str):
    for player in LOGGED_IN_PLAYERS:
        player.send_client_message(Color.RED, message)
