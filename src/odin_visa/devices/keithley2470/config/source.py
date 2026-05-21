from odin_visa.tree import Leaf, ParameterTreeMixin
from odin_visa.types import StrEnum, parse_enum, parse_float
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class SourceFunction(StrEnum):
    VOLTAGE = "VOLT"
    CURRENT = "CURR"
    INVALID = "INVALID"


# TODO: Remaining source parameters
class Source(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self._device = device

        self.set_function(SourceFunction.VOLTAGE)
        self.set_level(0.0)
        self.set_limit(0.1)

    def get_function(self) -> SourceFunction:
        return self.function

    def set_function(self, function: SourceFunction):
        self._device.write(f":SOUR:FUNC {function}")
        self.function = function

    def get_level(self) -> float:
        return self.level

    def set_level(self, level: float):
        if self.function == SourceFunction.INVALID:
            return

        self._device.write(f":SOUR:{self.function} {level}")
        self.level = level

    def get_limit(self) -> float:
        return self.limit

    def set_limit(self, limit: float):
        match self.function:
            case SourceFunction.INVALID:
                return
            case SourceFunction.CURRENT:
                limit_function = "V"
            case SourceFunction.VOLTAGE:
                limit_function = "I"

        self._device.write(f":SOUR:{self.function}:{limit_function}LIMIT {limit}")
        self.limit = limit

    def _get_function(self) -> SourceFunction:
        response = self._device.query(":SOUR:FUNC?") or ""
        return parse_enum(
            response.split(":")[0], SourceFunction, SourceFunction.INVALID
        )

    def _get_level(self) -> float:
        if self.function == SourceFunction.INVALID:
            return 0.0

        return parse_float(self._device.query(f":SOUR:{self.function}?"))

    def _get_limit(self) -> float:
        match self.function:
            case SourceFunction.INVALID:
                return 0.0
            case SourceFunction.CURRENT:
                limit_function = "V"
            case SourceFunction.VOLTAGE:
                limit_function = "I"

        return parse_float(
            self._device.query(f":SOUR:{self.function}:{limit_function}LIMIT?")
        )

    def update(self):
        self.function = self._get_function()
        self.level = self._get_level()
        self.limit = self._get_limit()

    function = Leaf(SourceFunction, get_function, set_function)
    level = Leaf(float, get_level, set_level)
    limit = Leaf(float, get_limit, set_limit)
    # range = Leaf(float, get_range, set_range)
    # auto_range = Leaf(bool, get_auto_range, set_auto_range)
    # delay = Leaf(int, get_delay, set_delay)
    # auto_delay = Leaf(bool, get_auto_delay, set_auto_delay)
