from pysamp import set_timer
from python.player.player import Player
from python.utils.vars import VEHICLES, VEHICLE_VARIABLES
from python.vehicle.functions import reload_vehicle
from python.vehicle.vehicle import Vehicle

@Vehicle.on_spawn
def on_spawn(vehicle: Vehicle):
    return

@Vehicle.on_death
@Vehicle.using_registry
def on_death(vehicle: Vehicle, killer: Player):

    db_id: int = vehicle.db_id

    if vehicle.is_registered:
        vehicle.update_panels_damage(3, 3, 3, 3, 3, 3, 3)
        vehicle.update_doors_damage(4, 4, 4, 4)
        vehicle.update_lights_damage(1, 1, 1)
        vehicle.update_tires_damage(1, 1, 1, 1)
        vehicle.health = 250.0

        set_timer(reload_vehicle, 2000, False, db_id)

        vehicle.destroy()

        VEHICLES[vehicle.id] = None
        VEHICLE_VARIABLES[vehicle.id] = None
