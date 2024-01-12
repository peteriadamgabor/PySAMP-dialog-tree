from sqlalchemy import text

from pysamp import register_callback, set_game_mode_text
from pystreamer import register_callbacks
from pystreamer.dynamiczone import DynamicZone

from python.model.database import HouseModel, VehicleData, Teleport, DutyLocation
from python.server.database import MAIN_SESSION
from python.model.server import House
from python.server.map_loader import load_maps, load_gates
from python.utils.vars import *
from python.utils.enums.zone_type import ZoneType
from python.model.server import Vehicle


def server_start():
    set_game_mode_text("FayRPG 4.0")

    load_houses()
    load_vehicles()
    load_teleports()
    load_duty_locations()

    print("Start load maps and gates")

    load_maps()
    load_gates()

    print("End load maps and gates")


def set_up_py_samp():
    register_callbacks()
    register_callback("OnPlayerFinishedDownloading", "ii")
    register_callback("OnPlayerRequestDownload", "iii")
    register_callback("OnCheatDetected", "isii")


def load_teleports():
    with MAIN_SESSION() as session:
        teleports = session.query(Teleport).all()

        for i in range(len(teleports)):
            teleport = teleports[i]
            zone = DynamicZone.create_sphere(teleport.from_x, teleport.from_y, teleport.from_z,
                                             1.0, world_id=teleport.from_vw, interior_id=teleport.from_interior)

            ZONES[zone.id] = (zone, ZoneType.TELEPORT)
            teleport.in_game_id = zone.id

        session.commit()


def load_duty_locations():
    with MAIN_SESSION() as session:
        duty_locations = session.query(DutyLocation).all()

        for i in range(len(duty_locations)):
            duty_location = duty_locations[i]
            zone = DynamicZone.create_sphere(duty_location.x, duty_location.y, duty_location.z, duty_location.size,
                                             world_id=duty_location.virtual_word, interior_id=duty_location.interior)

            ZONES[zone.id] = (zone, ZoneType.DUTY_LOCATION)
            duty_location.in_game_id = zone.id

        session.commit()


def load_houses():
    with MAIN_SESSION() as session:
        house_models = session.query(HouseModel).all()

        for i in range(len(house_models)):
            house_model = house_models[i]
            HOUSES.append(House(house_model.id))


def load_vehicles():
    with MAIN_SESSION() as session:
        vehicle_datas = session.query(VehicleData).all()

        for i in range(len(vehicle_datas)):
            vehicle_data = vehicle_datas[i]
            vehicle_data.in_game_id = i + 1

        session.commit()

    with MAIN_SESSION() as session:
        vehicle_datas = session.query(VehicleData).all()

        for i in range(len(vehicle_datas)):
            vehicle_data = vehicle_datas[i]

            model_id: int = vehicle_data.model_id + 399
            x: float = vehicle_data.x
            y: float = vehicle_data.y
            z: float = vehicle_data.z
            angle: float = vehicle_data.angle
            color_1: int = vehicle_data.color_1
            color_2: int = vehicle_data.color_2

            veh = Vehicle.create(model_id, x, y, z, angle, color_1, color_2, 5000)
            veh.set_number_plate(vehicle_data.plate)

            veh.is_registered = True

            VEHICLES[veh.id] = veh
