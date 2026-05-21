from odin_visa.devices.keithley2470.config.mode.loop_until_trigger import (
    LoopUntilTrigger,
)
from odin_visa.tree import ParameterTreeMixin, SubTree
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class Mode(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self.loop_until_trigger = LoopUntilTrigger(device)

    loop_until_trigger = SubTree(LoopUntilTrigger)
