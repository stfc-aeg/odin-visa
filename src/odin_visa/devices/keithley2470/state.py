from pickle import TRUE
from datetime import datetime, timezone
from odin_visa.devices.device_config import DeviceType
from odin_visa.devices.keithley2470.types import (
    Event,
    AveragingType,
    SenseFunction,
    SourceFunction,
    TriggerModelStatus,
)
import pandas as pd
from dataclasses import dataclass, field


@dataclass
class SourceConfigState:
    function: SourceFunction = SourceFunction.VOLTAGE
    level: float = 0.0
    limit: float = 0.1


@dataclass
class SenseConfigState:
    function: SenseFunction = SenseFunction.CURRENT
    auto_range: bool = True
    count: int = 1
    nplcs: float = 0.1
    range: float = 0.1
    averaging_enable: bool = False
    averaging_type: AveragingType = AveragingType.REPEATING
    averaging_count: int = 1


@dataclass
class SaveFileConfigState:
    file: str = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}.hdf5"
    subfolder: str = ""


@dataclass
class ConfigState:
    source: SourceConfigState = SourceConfigState()
    sense: SenseConfigState = SenseConfigState()
    savefile: SaveFileConfigState = SaveFileConfigState()


@dataclass
class EventLogState:
    count: int = 0
    last_event: Event | None = None
    log: list[Event] = field(default_factory=list)


@dataclass
class StatusState:
    block: int = 1
    status: TriggerModelStatus = TriggerModelStatus.EMPTY
    second_status: TriggerModelStatus = TriggerModelStatus.EMPTY


@dataclass
class BufferState:
    buffer: pd.DataFrame | None = None
    start_from: int = 0


@dataclass
class K2470State:
    kind: DeviceType
    ident: str
    address: str
    poll_freq: float = 1
    config: ConfigState = ConfigState()
    event_log: EventLogState = EventLogState()
    status: StatusState = StatusState()
    buffers: BufferState = BufferState()
