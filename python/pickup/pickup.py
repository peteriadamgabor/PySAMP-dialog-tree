from pysamp import call_native_function
from pysamp.pickup import Pickup as BasePickup
from python.utils.pickuptype import PickupType


class Pickup(BasePickup):

    def __int__(self, pickup_id: int, type: PickupType = None):
        super().__init__(pickup_id)

        self._type: PickupType = type

    def set_model(self, model_id):
        return call_native_function("SetPickupModel", self.id, model_id, True)
