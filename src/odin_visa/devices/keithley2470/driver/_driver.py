from typing import Any

import structlog

from odin_visa.devices.keithley2470.driver._query import SCPIQuery
from odin_visa.devices.keithley2470.driver.error import IncorrectResponseCountError
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

    async def execute(self, queries: list[SCPIQuery]) -> tuple[Any, ...]:
        cmd = ""
        for query in queries:
            cmd += f"{query.query};"

        logger.debug("Sending batch query to device", query=cmd)
        res = await self.transport.query(cmd)
        split = res.split(";")
        logger.debug("Device responded to batch query", query=cmd, responses=res)
        if len(split) != len(queries):
            raise IncorrectResponseCountError(cmd, len(queries), len(split))

        parsed = []
        for i, query in enumerate(queries):
            parsed.append(query.parser(split[i]))
        logger.debug("Parsed all the device queries", parsed=parsed)
        return tuple(parsed)
