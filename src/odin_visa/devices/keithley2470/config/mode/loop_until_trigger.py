from typing import TYPE_CHECKING
from odin_visa.devices.keithley2470.config.buffer import BufferConfig
from odin_visa.devices.keithley2470.acquisitions.types import AcquisitionType
from odin_visa.tree import Leaf, ParameterTreeMixin

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.config.mode import Mode
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class LoopUntilTrigger(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self._device = device

        self.post_trigger_reading_percentage = 100
        self.delay = 0

    def set_post_trigger_reading_percentage(self, percentage: int):
        self.post_trigger_reading_percentage = percentage

    def set_delay(self, delay: int):
        self.delay = delay

    def _load(self):
        self._device.write(
            f':TRIG:LOAD "LoopUntilEvent", COMM, {self.post_trigger_reading_percentage}, {self.delay}, "{self._device.config.buffer.name}"'
        )

    post_trigger_reading_percentage = Leaf(int, set=set_post_trigger_reading_percentage)
    delay = Leaf(int, set=set_delay)
