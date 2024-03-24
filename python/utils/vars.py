from typing import Any

from pysamp import get_max_players

SKINS: list = []

ZONES: dict[int, Any] = dict()

PLAYER_VARIABLES: list = [None] * get_max_players()
LOGGED_IN_PLAYERS: list = [None] * get_max_players()
ADMIN_PLAYERS: dict = {}

HOUSES: dict = {}
HOUSE_TYPES: list = []

BUSINESSES: dict = {}

PLAYER_COMMAND: dict = {}

ITEMS: list = []

VEHICLE_MODELS: list = [None] * 213
VEHICLE_VARIABLES: list = [None] * 2001
VEHICLES: list = [None] * 2001

PERMISSION_TYPES: list = []
ROLES: list = []
COMMAND_PERMISSIONS: dict = {}

FRACTIONS: list = [None] * 31
FRACTIONS_BY_CODE: dict = {}

PICKUPS: dict = {}
DYNAMIC_PICKUPS: dict = {}

INTERIORS: dict = {}

STATIC_OBJECTS: list = []
DYNAMIC_OBJECTS: list = []

GATES: list = []
