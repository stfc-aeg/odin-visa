from typing import TypedDict

from odin_visa.types import StrEnum


class DownsampledBufferConfig(TypedDict):
    name: str
    stride: int


class DeviceType(StrEnum):
    K2470 = "K2470"


class DeviceConfig(TypedDict):
    name: str
    type: DeviceType
    address: str
    buffers: list[DownsampledBufferConfig]


class DevicesConfig(TypedDict):
    devices: list[DeviceConfig]
