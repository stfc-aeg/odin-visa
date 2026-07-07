from dataclasses import dataclass
from enum import IntEnum

from dataclass_wizard import JSONSerializable

from odin_visa.types import StrEnum


# TODO: Is the event type a bitfield?
#        - Can there be an event that is both ERROR and WARNING?
class EventType(IntEnum):
    ERROR = 1
    WARNING = 2
    INFORMATION = 4


@dataclass
class Event(JSONSerializable):
    code: int
    message: str
    kind: EventType
    timestamp_ms: int
    context: str


class SenseFunction(StrEnum):
    VOLTAGE = "VOLTAGE"
    CURRENT = "CURRENT"


class AveragingType(StrEnum):
    REPEAT = "REPEAT"
    MOVING = "MOVING"


class SourceFunction(StrEnum):
    VOLTAGE = "VOLTAGE"
    CURRENT = "CURRENT"


class ProtectionLevel(StrEnum):
    PROT20 = "PROT20"
    PROT40 = "PROT40"
    PROT100 = "PROT100"
    PROT200 = "PROT200"
    PROT300 = "PROT300"
    PROT400 = "PROT400"
    PROT500 = "PROT500"
    NONE = "NONE"


class TriggerModelStatus(StrEnum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    PAUSED = "PAUSED"
    EMPTY = "EMPTY"
    BUILDING = "BUILDING"
    FAILED = "FAILED"
    ABORTING = "ABORTING"
    ABORTED = "ABORTED"
