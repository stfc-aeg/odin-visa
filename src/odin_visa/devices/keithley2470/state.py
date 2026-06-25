from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from odin_visa.devices.device_config import DeviceType
from odin_visa.devices.keithley2470.types import (
    AveragingType,
    Event,
    ProtectionLevel,
    SenseFunction,
    SourceFunction,
    TriggerModelStatus,
)


@dataclass
class SourceConfigState:
    delay: float = 0.0
    auto_delay: bool = False
    high_capacitance: bool = False
    level: float = 0.0
    limit: float = 0.1
    limit_tripped: bool = False
    function: SourceFunction = SourceFunction.VOLTAGE
    protection: ProtectionLevel = ProtectionLevel.PROT20
    protection_tripped: bool = False
    range: float = 2.0
    auto_range: bool = False
    read_back: bool = True


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
    base_folder: str = ""

    def path(self) -> Path:
        return Path(self.base_folder).joinpath(self.subfolder).joinpath(self.file)


@dataclass
class ConfigState:
    source: SourceConfigState = field(default_factory=SourceConfigState)
    sense: SenseConfigState = field(default_factory=SenseConfigState)
    savefile: SaveFileConfigState = field(default_factory=SaveFileConfigState)


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
    poll_freq: float = 1.0
    config: ConfigState = field(default_factory=ConfigState)
    event_log: EventLogState = field(default_factory=EventLogState)
    status: StatusState = field(default_factory=StatusState)
    buffers: BufferState = field(default_factory=BufferState)
