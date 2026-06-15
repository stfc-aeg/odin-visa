from __future__ import annotations
import logging
from tracemalloc import start
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

    def get_buffer(self):
        try:
            return self._buffer_manager.get_buffer(
                start=self.start_from,
                resample_method=self._resample_method,
                bin_size=self._bin_size,
            )
        except Exception as e:
            logging.warning("Could not read from buffer: %s", e)


class Buffers(ParameterTreeMixin):
    def __init__(self, device: "K2470Device", buffer_manager: BufferManager):
        self._device = device
        self._buffer_manager = buffer_manager
        self.start_from = 0

        self.buffers = {}
        for buffer_config in self._device._config.buffers:
            self.buffers[buffer_config.name] = Buffer(
                buffer_manager,
                buffer_config.resample_bin_size,
                buffer_config.resample_method,
            )

    def set_start_from(self, start_from: int):
        logging.info(f"old {self.start_from} | new {start_from}")
        self.start_from = start_from
        for _, buffer in self.buffers.items():
            buffer.start_from = start_from

    def as_tree(self) -> ParameterTree:
        buffers = ParameterTree(
            {name: (buffer.get_buffer, None) for name, buffer in self.buffers.items()}
        )
        start_from = ParameterTree(
            {"timestamp": (lambda: self.start_from, self.set_start_from)}
        )
        return ParameterTree({"buffers": buffers, "start_from": start_from})
