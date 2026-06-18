import logging
from .source import SourceDriver
from ..transport import K2470Transport


class K2470Driver:
    def __init__(self, transport: K2470Transport):
        logging.debug("initialising K2470Driver")
        self.source = SourceDriver(transport)
        logging.debug("initialised K2470Driver")
