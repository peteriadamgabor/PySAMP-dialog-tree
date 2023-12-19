from python.permission.permission_type import PermissionType
from python.utils.vars import PERMISSION_TYPES


class Permission:

    def __init__(self, type_id: int, power: int):
        self._permission_type: PermissionType = PERMISSION_TYPES[type_id - 1]
        self._power: int = power

    @property
    def permission_type(self):
        return self._permission_type

    @property
    def power(self):
        return self._power
