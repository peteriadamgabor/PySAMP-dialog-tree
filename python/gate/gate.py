from dataclasses import dataclass
from typing import List

from python.fraction.fraction import Fraction
from python.gate.gate_object import GateObject
import threading

@dataclass
class Gate:
    speed: int
    auto: bool
    close_time: int

    fractions: List[Fraction] = None
    objects: List[GateObject] = None

    timer: threading.Timer | None = None

    def open(self):
        print("open")
        for gate_object in self.objects:
            gate_object.move_to_open(self.speed)

        if self.auto:
            self.timer = threading.Timer(self.close_time, self.__timed_closed)
            self.timer.start()

    def close(self):
        print("close")
        for gate_object in self.objects:
            gate_object.move_to_close(self.speed)

    def __timed_closed(self):
        for gate_object in self.objects:
            gate_object.move_to_close(self.speed)

        self.timer.cancel()
        self.timer = None
