from odin_visa.tree import Leaf, ParameterTreeMixin
from odin_visa.types import StrEnum, parse_int
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class TriggerModelState(StrEnum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    EMPTY = "EMPTY"
    BUILDING = "BUILDING"
    FAILED = "FAILED"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"


class Status(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self._device = device
        self.update()

    def update(self):
        status_str = self._device.query(":TRIG:STAT?")
        if status_str == None:
            return None
        status_parts = status_str.split(";")
        self.state = TriggerModelState(status_parts[0])
        self.second_state = TriggerModelState(status_parts[1])
        self.block = parse_int(status_parts[2], 0)

    state = Leaf(TriggerModelState)
    second_state = Leaf(TriggerModelState)
    block = Leaf(int)
