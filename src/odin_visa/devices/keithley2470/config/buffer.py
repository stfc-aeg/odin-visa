from types import NoneType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device
from odin_visa.tree import Leaf, ParameterTreeMixin
from odin_visa.types import parse_int


class BufferConfig(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self.device = device

        self.name = "odinbuf"
        self.size = 2500

        self._create_buffer(self.name, self.size)

    def update(self):
        self.size = self.get_size()

    def set_name(self, name: str) -> None:
        """Renames the reading buffer. The old buffer is not deleted."""
        self.device.write(f':TRAC:MAKE "{name}", {self.size}')
        self.device.write(f':TRAC:FILL:MODE CONT, "{self.name}"')
        self.name = name

    def set_size(self, size: int) -> None:
        """Resizes the reading buffer, clearing any exisiting data"""
        self.device.write(f':TRAC:POIN {size}, "{self.name}"')
        self.size = self.get_size()

    def get_name(self) -> str:
        return self.name

    def get_size(self) -> int:
        return parse_int(self.device.query(f':TRAC:POIN? "{self.name}"'))

    def _clear(self, _):
        """Clears the current buffer"""
        self.device.write(f':TRAC:DEL "{self.name}"')
        self._create_buffer(self.name, self.size)

    def _create_buffer(self, name: str, size: int):
        self.device.write(f':TRAC:MAKE "{name}", {size}')
        self.device.write(f':TRAC:FILL:MODE CONT, "{name}"')

    name = Leaf(str, get_name, set_name)
    size = Leaf(int, get_size, set_size)
    clear = Leaf(NoneType, None, _clear)
