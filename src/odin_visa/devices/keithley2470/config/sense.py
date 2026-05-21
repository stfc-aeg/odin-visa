from __future__ import annotations
from odin_visa.tree import Leaf, ParameterTreeMixin, SubTree
from odin_visa.types import StrEnum, parse_bool, parse_enum, parse_float, parse_int
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class SenseFunction(StrEnum):
    VOLTAGE = "VOLT"
    CURRENT = "CURR"
    INVALID = "INVALID"


class AveragingType(StrEnum):
    REPEATING = "REP"
    MOVING = "MOV"
    INVALID = "INVALID"


class Averaging(ParameterTreeMixin):
    def __init__(self, device: "K2470Device", sense: Sense):
        self._sense = sense
        self._device = device

        self.set_enable(False)
        self.set_count(1)
        self.set_type(AveragingType.REPEATING)

    def get_enable(self) -> bool:
        return self.enable

    def set_enable(self, enable: bool):
        if self._sense.function == SenseFunction.INVALID:
            return

        state = "ON" if enable else "OFF"
        self._device.write(f":SENS:{self._sense.function}:AVER {state}")
        self.enable = enable

    def get_count(self) -> int:
        return self.count

    def set_count(self, count):
        if self._sense.function == SenseFunction.INVALID:
            return

        self._device.write(f":SENS:{self._sense.function}:AVER:COUN {count}")
        self.count = count

    def get_type(self) -> AveragingType:
        return self.type

    def set_type(self, type: AveragingType):
        if self._sense.function == SenseFunction.INVALID:
            return

        self._device.write(f":SENS:{self._sense.function}:AVER:TCON {type}")
        self.type = type

    def _get_enable(self) -> bool:
        if self._sense.function == SenseFunction.INVALID:
            return False

        return parse_bool(
            self._device.query(f":SENS:{self._sense.function}:AVER:TCON?")
        )

    def _get_count(self) -> int:
        if self._sense.function == SenseFunction.INVALID:
            return 0

        return parse_int(self._device.query(f":SENS:{self._sense.function}:AVER:COUN?"))

    # TODO: error log for invalid types + other adapter errors?
    def _get_type(self) -> AveragingType:
        if self._sense.function == SenseFunction.INVALID:
            return AveragingType.INVALID

        return parse_enum(
            self._device.query(f":SENS:{self._sense.function}:AVER:TCON?"),
            AveragingType,
            AveragingType.INVALID,
        )

    def update(self):
        self.enable = self._get_enable()
        self.count = self._get_count()
        self.type = self._get_type()

    enable = Leaf(bool, get_enable, set_enable)
    count = Leaf(int, get_count, set_count)
    type = Leaf(AveragingType, get_type, set_type)


# TODO: Add all the sense params
class Sense(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self._device = device

        self.set_function(SenseFunction.CURRENT)
        self.set_nplcs(1.0)
        self.set_range(0.1)
        self.set_auto_range(False)
        self.set_count(1)
        self.averaging = Averaging(device, self)

    def get_function(self) -> SenseFunction:
        return self.function

    def set_function(self, function: SenseFunction):
        self._device.write(f':SENSE:FUNC "{function}"')
        self.function = function

    def get_nplcs(self) -> float:
        return self.nplcs

    def set_nplcs(self, nplcs: float):
        if self.function == SenseFunction.INVALID:
            return

        self._device.write(f":SENSE:{self.function}:NPLC {nplcs}")
        self.nplcs = nplcs

    def get_range(self) -> float:
        return self.range

    def set_range(self, range: float):
        if self.function == SenseFunction.INVALID:
            return

        self._device.write(f":SENSE:{self.function}:RANGE {range}")
        self.range = range

    def get_auto_range(self) -> bool:
        return self.auto_range

    def set_auto_range(self, enable: bool):
        if self.function == SenseFunction.INVALID:
            return

        enable_str = "ON" if enable else "OFF"
        self._device.write(f":SENSE:{self.function}:RANGE:AUTO {enable_str}")
        self.auto_range = enable

    def get_count(self) -> int:
        return self.count

    def set_count(self, count: int):
        self._device.write(f":SENSE:COUNT {count}")
        self.count = count

    def _get_function(self) -> SenseFunction:
        response = self._device.query(":SENS:FUNC?") or ""
        # device can respond with ':DC' suffix, so we need to ignore that
        function = parse_enum(
            response.split(":")[0], SenseFunction, SenseFunction.INVALID
        )
        return function

    def _get_nplcs(self) -> float:
        if self.function == SenseFunction.INVALID:
            return 0.0

        return parse_float(self._device.query(f":SENSE:{self.function}:NPLC?"))

    def _get_range(self) -> float:
        if self.function == SenseFunction.INVALID:
            return 0.0

        return parse_float(self._device.query(f":SENSE:{self.function}:RANGE?"))

    def _get_auto_range(self) -> bool:
        if self.function == SenseFunction.INVALID:
            return False

        return parse_bool(self._device.query(f":SENSE:{self.function}:RANGE:AUTO?"))

    def _get_count(self) -> int:
        return parse_int(self._device.query(f":SENSE:COUNT?"))

    def update(self):
        self.function = self._get_function()
        self.nplcs = self._get_nplcs()
        self.range = self._get_range()
        self.auto_range = self._get_auto_range()
        self.count = self._get_count()
        self.averaging.update()

    function = Leaf(SenseFunction, get_function, set_function)
    nplcs = Leaf(float, get_nplcs, set_nplcs)
    range = Leaf(float, get_range, set_range)
    auto_range = Leaf(bool, get_auto_range, set_auto_range)
    count = Leaf(int, get_count, set_count)
    averaging = SubTree(Averaging)
