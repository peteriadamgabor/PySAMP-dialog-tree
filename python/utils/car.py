from sqlalchemy import text

from python.server.database import UTIL_ENGINE


def get_model_id_by_name(name: str) -> int | None:
    with (UTIL_ENGINE.connect() as conn):

        query: text = text("SELECT id FROM vehicle_models WHERE name ILIKE :name LIMIT 1")
        result = conn.execute(query, {"name": name+"%"}).one_or_none()

    return result[0] + 399 if result else None
