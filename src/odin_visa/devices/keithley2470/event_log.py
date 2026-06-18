from dataclasses import dataclass
from dataclass_wizard import JSONSerializable
from enum import IntEnum
from time import mktime, strptime
from typing import List, TypedDict

from odin_visa.tree import Leaf, ParameterTreeMixin
from odin_visa.types import parse_int


class EventLog(ParameterTreeMixin):
    def __init__(self):
        self.count = 0
        self.log = []
        self.last_event = None

    def push_event(self, event_str: str, context: str = ""):
        # events are in the format "<code>,<message>;<type>;<datetime>"
        event_str = event_str.replace('"', "")
        split = event_str.split(";")
        code_message = split[0].split(",")
        event = Event(
            code=parse_int(code_message[0], 0),
            message=code_message[1],
            kind=EventType(int(split[1])),
            timestamp_ms=self._parse_datetime(split[2]),
            context=context,
        )
        self.count += 1
        self.log.append(event)
        self.last_event = event

    def _parse_datetime(self, datetime: str) -> int:
        # example datetime: 2026/05/12 12:55:33.648
        # strptime() doesn't support parsing milliseconds, so we get/trim it ourself
        milliseconds = parse_int(datetime[-3:], 0)
        datetime = datetime[:-4]
        format = "%Y/%m/%d %H:%M:%S"
        timestamp_seconds = int(mktime(strptime(datetime, format)))
        return timestamp_seconds * 1000 + milliseconds

    count = Leaf(int, None, None)
    log = Leaf(List[Event], None, None)
    last_event = Leaf(Event, None, None)
