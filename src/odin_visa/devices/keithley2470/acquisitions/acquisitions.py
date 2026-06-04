from types import NoneType
from odin_visa.devices.keithley2470.acquisitions.buffers import Buffers
from odin_visa.devices.keithley2470.acquisitions.status import Status, TriggerModelState
from odin_visa.devices.keithley2470.acquisitions.types import AcquisitionType
from odin_visa.devices.keithley2470.config.config import Config
from odin_visa.devices.keithley2470.managers.buffer_manager import BufferManager
from odin_visa.devices.keithley2470.managers.savefile_manager import SaveFileManager
from odin_visa.tree import Leaf, ParameterTreeMixin, SubTree
from typing import TYPE_CHECKING

from odin_visa.types import parse_bool

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class Acquisitions(ParameterTreeMixin):
    def __init__(self, device: "K2470Device", config: Config):
        self._device = device
        self._config = config

        self.type = AcquisitionType.LOOP_UNTIL_TRIGGER
        self.status = Status(device)
        self.set_output(False)
        self.paused = True

    def do_clear(self, _):
        self._config.buffer._clear(_)

    def do_start(self, _):
        self.paused = False

        self._config.buffer._clear(_)
        match self.type:
            case AcquisitionType.LOOP_UNTIL_TRIGGER:
                self._config.mode.loop_until_trigger._load()

        self._device.write("INIT")

        self._device._buffer_manager.start_acquisition()

    def do_stop(self, _):
        self.paused = True

        match self.type:
            case AcquisitionType.LOOP_UNTIL_TRIGGER:
                self._device.write("*TRG")

        self._device._buffer_manager.stop_acquisition()

    def set_output(self, output: bool):
        self._device.write(f":OUTP {int(output)}")
        self.output = output

    def set_type(self, type: AcquisitionType):
        self.type = type

    def set_paused(self, pause: bool):
        if pause == self.paused:
            return

        if self.status.state != TriggerModelState.EMPTY:
            if pause:
                self._device.write("*TRG")
                self.paused = True
            else:
                self._device.write(":INIT")
                self.paused = False

    def _get_output(self) -> bool:
        return parse_bool(self._device.query(":OUTP?"))

    def update(self):
        self.output = self._get_output()
        self.status.update()

    def cleanup(self):
        self.paused = True

    type = Leaf(AcquisitionType, set=set_type)
    output = Leaf(bool, set=set_output)
    clear = Leaf(NoneType, set=do_clear)
    start = Leaf(NoneType, set=do_start)
    stop = Leaf(NoneType, set=do_stop)
    paused = Leaf(bool, set=set_paused)
    status = SubTree(Status)
