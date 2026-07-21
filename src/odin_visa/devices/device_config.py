from dataclasses import dataclass
from typing import Any

from dataclass_wizard import JSONSerializable

from odin_visa.devices.device import DeviceType


@dataclass
class DeviceConfig(JSONSerializable):
    name: str
    type: DeviceType
    address: str


@dataclass
class DevicesConfig(JSONSerializable):
    devices: list[dict[str, Any]]
