from dataclasses import dataclass, field

import hdf5plugin
from dataclass_wizard import JSONSerializable

from odin_visa.devices.device_config import DeviceConfig
from odin_visa.devices.keithley2470.state import ConfigState
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


class Blosc2Filters(StrEnum):
    NOFILTER = "none"
    SHUFFLE = "shuffle"
    BITSHUFFLE = "bitshuffle"
    DELTA = "delta"
    TRUNC_PREC = "trunc_prec"

    def tofilter(self) -> int:
        match self:
            case Blosc2Filters.NOFILTER:
                return hdf5plugin.Blosc2.NOFILTER
            case Blosc2Filters.SHUFFLE:
                return hdf5plugin.Blosc2.SHUFFLE
            case Blosc2Filters.BITSHUFFLE:
                return hdf5plugin.Blosc2.BITSHUFFLE
            case Blosc2Filters.DELTA:
                return hdf5plugin.Blosc2.DELTA
            case Blosc2Filters.TRUNC_PREC:
                return hdf5plugin.Blosc2.TRUNC_PREC


@dataclass
class Blosc2Config(JSONSerializable):
    filter: Blosc2Filters
    clevel: int = 3
    cname: str = "zstd"


class CompressionType(StrEnum):
    GZIP = "gzip"
    LZF = "lzf"
    SZIP = "szip"
    BLOSC2 = "blosc2"
    NONE = "none"


@dataclass
class CompressionConfig:
    type: CompressionType
    settings: Blosc2Config | None = None


@dataclass
class SaveFileConfig(JSONSerializable):
    data_folder: str = "/data"
    save_frequency: int = 10
    measurements_compression: CompressionConfig = field(
        default_factory=lambda: CompressionConfig(
            type=CompressionType.BLOSC2,
            settings=Blosc2Config(
                filter=Blosc2Filters.SHUFFLE,
                clevel=3,
                cname="zstd",
            ),
        )
    )
    timestamp_compression: CompressionConfig = field(
        default_factory=lambda: CompressionConfig(
            type=CompressionType.BLOSC2,
            settings=Blosc2Config(
                filter=Blosc2Filters.BITSHUFFLE,
                clevel=3,
                cname="zstd",
            ),
        )
    )


@dataclass
class DeviceBuffer(JSONSerializable):
    name: str = "odin_buffer"
    size: int = 50000


@dataclass
class K2470DeviceConfig(DeviceConfig):
    default_state: ConfigState = field(default_factory=ConfigState)
    device_buffer: DeviceBuffer = field(default_factory=DeviceBuffer)
    savefile_config: SaveFileConfig = field(default_factory=SaveFileConfig)
