from dataclass_wizard import JSONSerializable
from dataclasses import dataclass
from odin_visa.types import StrEnum


@dataclass
class DownsampledBufferConfig(JSONSerializable):
    name: str
    resample_bin_size: str | None = None
    resample_method: str | None = None


class DeviceType(StrEnum):
    K2470 = "K2470"


@dataclass
class SaveFileConfig(JSONSerializable):
    data_folder: str = "/data"


@dataclass
class DeviceConfig(JSONSerializable):
    name: str
    type: DeviceType
    address: str
    buffers: list[DownsampledBufferConfig]
    savefile_config: SaveFileConfig = SaveFileConfig()


@dataclass
class DevicesConfig(JSONSerializable):
    devices: list[DeviceConfig]
