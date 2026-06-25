from odin_visa.devices.keithley2470.transport import K2470Transport

from .buffer import BufferDriver
from .sense import SenseDriver
from .source import SourceDriver
from .trigger_model import TriggerModelDriver


class K2470Driver:
    def __init__(self, transport: K2470Transport) -> None:
        self.transport = transport
        self.buffer = BufferDriver(transport)
        self.trigger_model = TriggerModelDriver(transport)
        self.source = SourceDriver(transport)
        self.sense = SenseDriver(transport)

    async def reset(self) -> None:
        await self.transport.write("*RST")
        await self.transport.write("FORM REAL")
