from typing import List

from sqlalchemy import text

from python.permission.permission import Permission
from python.server.database import MAIN_ENGINE


class Role:
    def __init__(self, id: int, name: str):
        self._id: int = id
        self._name: str = name
        self._permissions: List[Permission] = self._load_permission()

    def _load_permission(self) -> List[Permission]:
        with MAIN_ENGINE.connect() as conn:
            query: text = text("SELECT permission_type_id, power FROM role_permissions "
                               "where role_id = :role_id;")
            rows = conn.execute(query, {'role_id': self._id}).fetchall()

            return [Permission(*row) for row in rows]

    def reload_permission(self):
        with MAIN_ENGINE.connect() as conn:
            query: text = text("SELECT permission_type_id, power FROM role_permissions "
                               "where role_id = :role_id;")
            rows = conn.execute(query, {'role_id': self._id}).fetchall()

            return [Permission(*row) for row in rows]

    @property
    def name(self) -> str:
        return self._name

    @property
    def permissions(self) -> List[Permission]:
        return self._permissions
