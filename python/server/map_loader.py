import json
import os

from pystreamer.dynamicobject import DynamicObject
from pysamp.object import Object
from python.gate.gate import Gate
from python.gate.gate_object import GateObject
from python.utils.vars import GATES, STATIC_OBJECTS, DYNAMIC_OBJECTS


def load_maps():
    for mapp in os.listdir("maps"):
        if mapp == 'example.json':
            continue

        with open(os.path.join("maps", mapp)) as f:

            objects = json.loads(f.read())

            for object in objects:
                if object["static"]:
                    s_object = Object.create(object["model_id"],
                                             object["x"], object["y"], object["z"],
                                             object["rotation_x"], object["rotation_y"], object["rotation_z"])

                    STATIC_OBJECTS.append(s_object)

                else:
                    d_object = DynamicObject.create(object["model_id"],
                                                    object["x"], object["y"], object["z"],
                                                    object["rotation_x"], object["rotation_y"], object["rotation_z"],
                                                    world_id=object["world_id"],
                                                    interior_id=object["interior_id"],
                                                    draw_distance=object["draw_distance"],
                                                    stream_distance=object["stream_distance"])

                    if "materials" in object:
                        for material in object["materials"]:
                            d_object.set_material(material["material_index"],
                                                  material["model_id"],
                                                  material["txd_name"],
                                                  material["texture_name"],
                                                  material["material_color"])

                    DYNAMIC_OBJECTS.append(d_object)

            print(f"| {mapp.replace('.json', '')} map successful loaded. Object Count: {len(objects)} ")


def load_gates():
    for mapp in os.listdir("gates"):
        if mapp == 'example.json':
            continue

        with open(os.path.join("gates", mapp)) as f:

            gates = json.loads(f.read())

            for gate in gates:
                speed: int
                auto: bool
                close_time: int

                py_gate: Gate = Gate(gate["speed"], gate["auto"], gate["close_time"])

                py_gate.objects = []

                for gate_object in gate["objects"]:
                    py_gate_object: GateObject = GateObject(
                        gate_object["model_id"],
                        gate_object["x"],
                        gate_object["y"],
                        gate_object["z"],
                        gate_object["rotation_x"],
                        gate_object["rotation_y"],
                        gate_object["rotation_z"],
                        gate_object["world_id"],
                        gate_object["interior_id"],
                        gate_object["draw_distance"],
                        gate_object["stream_distance"],
                        gate_object["move_x"],
                        gate_object["move_y"],
                        gate_object["move_z"],
                        gate_object["move_rotation_x"],
                        gate_object["move_rotation_y"],
                        gate_object["move_rotation_z"])

                    py_gate_object.create_object()

                    py_gate.objects.append(py_gate_object)

                GATES.append(py_gate)

            print(f"| {mapp.replace('.json', '')} gate successful loaded.")
