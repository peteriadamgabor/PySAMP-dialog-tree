from typing import List

from sqlalchemy import text

from pysamp import register_callback, set_game_mode_text
from pystreamer import register_callbacks

from python.model.database import HouseModel, VehicleData, Teleport, DutyLocation, Skin, BusinessModel, InteriorModel
from python.server.database import MAIN_SESSION
from python.model.server import House, DynamicZone, Business, Interior
from python.server.map_loader import load_maps, load_gates
from python.utils.vars import *
from python.utils.enums.zone_type import ZoneType
from python.model.server import Vehicle


def server_start():
    set_game_mode_text("FayRPG 5.0")

    load_houses()
    load_vehicles()
    load_teleports()
    load_duty_locations()
    load_business()
    load_interiors()

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

            zone.zone_type = ZoneType.TELEPORT

            ZONES[zone.id] = zone

            teleport.in_game_id = zone.id

        session.commit()


def load_duty_locations():
    with MAIN_SESSION() as session:
        duty_locations = session.query(DutyLocation).all()

        for i in range(len(duty_locations)):
            duty_location = duty_locations[i]
            zone = DynamicZone.create_sphere(duty_location.x, duty_location.y, duty_location.z, duty_location.size,
                                             world_id=duty_location.virtual_word, interior_id=duty_location.interior)

            zone.zone_type = ZoneType.DUTY_LOCATION

            ZONES[zone.id] = zone

            duty_location.in_game_id = zone.id

        session.commit()


def load_houses():
    with MAIN_SESSION() as session:
        house_models = session.query(HouseModel).all()

        for i in range(len(house_models)):
            house_model = house_models[i]
            house = House(house_model.id)

            HOUSES[house.pickup.id] = house


def load_business():
    with MAIN_SESSION() as session:
        business_models: List[BusinessModel] = session.query(BusinessModel).all()

        for i in range(len(business_models)):
            business_model: BusinessModel = business_models[i]
            business = Business(business_model.id)

            BUSINESSES[business.pickup.id] = business

            business.in_game_id = i


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


def load_interiors():
    with MAIN_SESSION() as session:
        interiors = session.query(InteriorModel).all()

        for i in range(len(interiors)):
            interior = interiors[i]

            INTERIORS[i] = Interior(i, interior.x, interior.y, interior.z,  interior.interior)

            interior.in_game_id = i

        session.commit()
