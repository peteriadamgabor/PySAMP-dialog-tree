from math import sqrt

from sqlalchemy import text

from python.model.server import Gate, GateObject, Player
from python.server.database import PLAYER_ENGINE
from python.utils.vars import LOGGED_IN_PLAYERS, GATES


def _find_player_by_name(name: str):
    return next((e for e in LOGGED_IN_PLAYERS if e is not None and name in e.get_name()), None)


def _find_player_by_id(id: int):
    return LOGGED_IN_PLAYERS[id]


def get_player(search_value: str | int):
    if not search_value:
        return None

    if type(search_value) is int or search_value.isdigit():
        return _find_player_by_id(int(search_value))

    else:
        return _find_player_by_name(search_value)


def check_is_valid_player(search_value: str | int):
    return get_player(search_value) is None


def find_player_in_db_by_name(search_value: str | int):
    if search_value.isdigit():
        return int(search_value)
    else:
        with PLAYER_ENGINE.connect() as conn:
            query: text = text("SELECT id FROM houses WHERE name ILIKE :property'")
            result = conn.execute(query, {'property': id}).fetchall()

            if result == 1:
                return result[0]

            return None


def get_nearest_gate(player_pos):
    nearest_gate: Gate = GATES[0]
    dist = calculate_dist(player_pos,
                          (nearest_gate.objects[0].x, nearest_gate.objects[0].y, nearest_gate.objects[0].z))

    for gate in GATES[1:]:
        gate_object: GateObject = gate.objects[0]

        now_dist = calculate_dist(player_pos, (gate_object.x, gate_object.y, gate_object.z))

        if dist > now_dist:
            dist = now_dist
            nearest_gate = gate

    if dist <= 5.0:
        return nearest_gate
    return None


def get_nearest_player(player: Player):

    nearest_player = player.streamed_players[0] if len(player.streamed_players) > 0 else None

    start_index: int = 0 if nearest_player is None else 1

    dist = 0.0

    if nearest_player:
        n_x, n_y, n_z = nearest_player.get_pos()
        p_x, p_y, p_z = player.get_pos()

        dist = calculate_dist((p_x, p_y, p_z), (n_x, n_y, n_z))

    for check_player in player.streamed_players[start_index:]:
        if check_player:
            n_x, n_y, n_z = check_player.get_pos()
            p_x, p_y, p_z = player.get_pos()

            new_dist = calculate_dist((p_x, p_y, p_z), (n_x, n_y, n_z))

            if dist > new_dist:
                dist = new_dist
                nearest_player = check_player

    if dist <= 5.0:
        return nearest_player
    return None


def calculate_dist(point1, point2):
    x, y, z = point1
    a, b, c = point2

    distance = sqrt(pow(a - x, 2) +
                    pow(b - y, 2) +
                    pow(c - z, 2) * 1.0)
    return distance
