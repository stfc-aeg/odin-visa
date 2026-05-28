from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from odin_control.adapters.parameter_tree import ParameterTree
from odin_visa.devices.keithley2470.managers.buffer_manager import BufferManager
from odin_visa.tree import Leaf, ParameterTreeMixin

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class Buffer(ParameterTreeMixin):
    def __init__(
        self,
        buffer_manager: BufferManager,
        bin_size: str | None,
        resample_method: str | None,
    ):
        self._buffer_manager = buffer_manager
        self._bin_size = bin_size
        self._resample_method = resample_method
        self.buffer = []
        self.start_from = 0

    def update(self):
        pass

    def get_buffer(self):
        return self._buffer_manager.get_buffer(
            start=self.start_from,
            resample_method=self._resample_method,
            bin_size=self._bin_size,
        )

    def set_start_from(self, start_from: int):
        self.start_from = start_from

    start_from = Leaf(int, set=set_start_from)
    buffer = Leaf(list[tuple[int, float, float]], get_buffer, None)


class Buffers(ParameterTreeMixin):
    def __init__(self, device: "K2470Device", buffer_manager: BufferManager):
        self._device = device
        self._buffer_manager = buffer_manager

        self.buffers = {}
        for buffer_config in self._device._config["buffers"]:
            self.buffers[buffer_config["name"]] = Buffer(
                buffer_manager,
                buffer_config.get("resample_bin_size"),
                buffer_config.get("resample_method"),
            )

    def as_tree(self) -> ParameterTree:
        logging.info(f"{self.buffers}")
        return ParameterTree(
            {name: buffer.as_tree() for name, buffer in self.buffers.items()}
        )

    def update(self):
        for _, buffer in self.buffers.items():
            buffer.update()
