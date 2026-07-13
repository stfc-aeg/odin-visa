from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from odin_visa.devices.device import DeviceType
from odin_visa.devices.keithley2470.types import (
    AveragingType,
    Event,
    ProtectionLevel,
    SenseFunction,
    SourceFunction,
    TriggerModelStatus,
)
from odin_visa.types import StrEnum


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
    averaging_count: int = 1
    averaging: bool = False
    averaging_type: AveragingType = AveragingType.REPEAT
    auto_zero: bool = False
    nplcs: float = 0.1
    offset_compensation: bool = False
    auto_range: bool = False
    auto_range_lower_limit: float = 10e-9
    auto_range_rebound: bool = False
    auto_range_upper_limit: float = 0.1
    range: float = 0.1
    relative_offset_level: float = 0
    relative_offset: bool = False
    remote_sensing: bool = False
    count: int = 1
    function: SenseFunction = SenseFunction.CURRENT


@dataclass
class SaveFileConfigState:
    file: str = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}.hdf5"
    subfolder: str = ""
    base_folder: str = ""

    def path(self) -> Path:
        return Path(self.base_folder).joinpath(self.subfolder).joinpath(self.file)


@dataclass
class AcquisitionState:
    acquiring: bool = False


class SMode(StrEnum):
    Normal = "NORMAL"
    HighImpedance = "HIMPEDANCE"
    Zero = "ZERO"
    Guard = "GUARD"


class Terminal(StrEnum):
    Front = "FRONT"
    Rear = "REAR"


@dataclass
class OutputState:
    smode: SMode = SMode.Normal
    interlock: bool = False
    interlock_tripped: bool = False
    enabled: bool = False
    terminals: Terminal = Terminal.Front


@dataclass
class ConfigState:
    acquisition: AcquisitionState = field(default_factory=AcquisitionState)
    source: SourceConfigState = field(default_factory=SourceConfigState)
    sense: SenseConfigState = field(default_factory=SenseConfigState)
    savefile: SaveFileConfigState = field(default_factory=SaveFileConfigState)
    output: OutputState = field(default_factory=OutputState)
    poll_freq: float = 1.0


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


class ResampleMethod(StrEnum):
    Full = "Full"
    Mean = "Mean"
    Median = "Median"
    Min = "Min"
    Max = "Max"
    First = "First"


@dataclass
class BufferState:
    buffer: pd.DataFrame | None = None
    range: int = 10
    downsample: ResampleMethod = ResampleMethod.Full
    # TODO: microseconds int?
    bin_size: str = "50ms"


@dataclass
class K2470State:
    kind: DeviceType
    ident: str
    address: str
    config: ConfigState
    event_log: EventLogState = field(default_factory=EventLogState)
    status: StatusState = field(default_factory=StatusState)
    buffer: BufferState = field(default_factory=BufferState)
