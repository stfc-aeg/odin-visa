from dataclasses import dataclass, field

from dataclass_wizard import JSONSerializable

from odin_visa.types import StrEnum


class ResampleMethod(StrEnum):
    Mean = "mean"
    Median = "median"
    Min = "min"
    Max = "max"
    First = "first"


@dataclass
class DownsampledBufferConfig(JSONSerializable):
    name: str
    resample_bin_size: str | None = None
    resample_method: ResampleMethod | None = None


class DeviceType(StrEnum):
    K2470 = "K2470"


@dataclass
class SaveFileConfig(JSONSerializable):
    data_folder: str = "/data"


@dataclass
class DeviceBuffer(JSONSerializable):
    name: str = "odin_buffer"
    size: int = 50000


@dataclass
class DeviceConfig(JSONSerializable):
    name: str
    type: DeviceType
    address: str
    buffers: list[DownsampledBufferConfig]
    device_buffer: DeviceBuffer = field(default_factory=DeviceBuffer)
    savefile_config: SaveFileConfig = field(default_factory=SaveFileConfig)


@dataclass
class DevicesConfig(JSONSerializable):
    devices: list[DeviceConfig]
