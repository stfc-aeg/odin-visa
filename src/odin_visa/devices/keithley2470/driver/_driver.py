import structlog

from odin_visa.devices.keithley2470.state import EventLogState
from odin_visa.devices.keithley2470.transport import K2470Transport

from .buffer import BufferDriver
from .output import OutputDriver
from .sense import SenseDriver
from .source import SourceDriver
from .trigger_model import TriggerModelDriver

logger = structlog.get_logger()


class K2470Driver:
    def __init__(self, transport: K2470Transport, event_log: EventLogState) -> None:
        self.transport = transport
        self.event_log = event_log
        self.buffer = BufferDriver(transport, event_log)
        self.trigger_model = TriggerModelDriver(transport, event_log)
        self.source = SourceDriver(transport, event_log)
        self.sense = SenseDriver(transport, event_log)
        self.output = OutputDriver(transport, event_log)
