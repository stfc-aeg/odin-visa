from odin_visa.devices.device_config import DeviceConfig
from odin_visa.devices.keithley2470.config.buffer import BufferConfig
from odin_visa.devices.keithley2470.config.mode.mode import Mode
from odin_visa.devices.keithley2470.config.savefile import SaveFileConfigTree
from odin_visa.devices.keithley2470.config.sense import Sense
from odin_visa.devices.keithley2470.config.source import Source
from odin_visa.tree import ParameterTreeMixin, SubTree
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class Config(ParameterTreeMixin):
    sense = SubTree(Sense)
    source = SubTree(Source)
    buffer = SubTree(BufferConfig)
    savefile = SubTree(SaveFileConfigTree)
    mode = SubTree(Mode)

    def __init__(self, device: "K2470Device", config: DeviceConfig):
        self.device = device

        self.sense = Sense(device)
        self.source = Source(device)
        self.buffer = BufferConfig(device)
        self.savefile = SaveFileConfigTree(device, config.savefile_config.data_folder)
        self.mode = Mode(device)

    def update(self, trigger_model_running: bool):
        self.buffer.update()
        self.savefile.update()
        if not trigger_model_running:
            self.sense.update()
            self.source.update()
