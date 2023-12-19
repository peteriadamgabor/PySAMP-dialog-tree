from sqlalchemy import text

from python.server.database import HOUSE_ENGINE


class HouseType:

    def __init__(self, id):
        with HOUSE_ENGINE.connect() as conn:
            query: text = text("SELECT enter_x, enter_y, enter_z, angle,"
                               " interior, description, price"
                               " FROM house_types WHERE id = :property")
            result = conn.execute(query, {'property': id}).fetchone()

            if result:
                self._id = id
                self._enter_x: float = result[0]
                self._enter_y: float = result[1]
                self._enter_z: float = result[2]
                self._angle: float = result[3]
                self._interior: int = result[4]
                self._description: str = result[5]
                self._price: int = result[6]

    @property
    def id(self):
        return self._id

    @property
    def enter_x(self):
        return self._enter_x

    @property
    def enter_y(self):
        return self._enter_y

    @property
    def enter_z(self):
        return self._enter_z

    @property
    def angle(self):
        return self._angle
    
    @property
    def interior(self):
        return self._interior

    @property
    def description(self):
        return self._description

    @property
    def price(self):
        return self._price
