
class PermissionType:

    def __init__(self, id: int, name: str, code: str):
        self._id: int = id
        self._name: str = name
        self._code: str = code

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code
