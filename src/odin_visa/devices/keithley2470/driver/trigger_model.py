import structlog

from odin_visa.devices.keithley2470.driver._catch_error import catch_error
from odin_visa.devices.keithley2470.state import EventLogState
from odin_visa.devices.keithley2470.transport import K2470Transport

logger = structlog.get_logger()


class TriggerModelDriver:
    def __init__(self, transport: K2470Transport, event_log: EventLogState) -> None:
        self.transport = transport
        self.event_log = event_log

    @catch_error
    async def load_loop_until_trigger_model(self, buffer_name: str) -> None:
        await self.transport.write(
            ':TRIG:LOAD "Empty";'  # load empty template
            f':TRIG:BLOCK:MDIG 1, "{buffer_name}";'  # make measurement into given buffer
            ":TRIG:BLOCK:BRANCH:EVENT 2, COMM, 0;"  # branch to block 0 (IDLE state) if trigger has been sent, otherwise continue
            ":TRIG:BLOCK:BRANCH:ALWAYS 3, 1"  # always branch to block 1 (measurement)
        )

    @catch_error
    async def trigger(self) -> None:
        await self.transport.write("*TRG")

    @catch_error
    async def init(self) -> None:
        await self.transport.write("INIT")
