from typing import Tuple, Any, Dict

from pysamp import get_max_players

SKINS = []

ZONES: Dict[int, Tuple[Any, Any]] = dict()

PLAYER_VARIABLES = [None] * get_max_players()
LOGGED_IN_PLAYERS = [None] * get_max_players()

HOUSES = []
HOUSE_TYPES = []

ITEMS = []

VEHICLE_MODELS = [None] * 213
VEHICLE_VARIABLES = [None] * 2001
VEHICLES = [None] * 2001

PERMISSION_TYPES = []
ROLES = []
COMMAND_PERMISSIONS = {}

FRACTIONS = [None] * 31
FRACTIONS_BY_CODE = {}

STATIC_OBJECTS = []
DYNAMIC_OBJECTS = []

GATES = []
