from odin_visa.devices.keithley2470.transport import K2470Transport

from .source import SourceDriver


class K2470Driver:
    def __init__(self, transport: K2470Transport) -> None:
        self.source = SourceDriver(transport)
