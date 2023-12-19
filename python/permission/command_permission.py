from python.permission.permission_type import PermissionType
from python.utils.vars import PERMISSION_TYPES


class CommandPermission:

    def __init__(self, cmd_txt: str, permission_type_id: int, power: int):
        self._cmd_txt: str = cmd_txt
        self._permission_type: PermissionType = PERMISSION_TYPES[permission_type_id - 1]
        self._need_power: int = power

    @property
    def permission_type(self):
        return self._permission_type

    @property
    def need_power(self):
        return self._need_power
