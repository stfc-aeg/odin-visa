from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from odin_control.adapters.parameter_tree import ParameterTree
from odin_visa.devices.keithley2470.managers.buffer_manager import BufferManager
from odin_visa.tree import Leaf, ParameterTreeMixin

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class Buffer(ParameterTreeMixin):
    def __init__(self, buffer_manager: BufferManager, stride: int):
        self._buffer_manager = buffer_manager
        self._stride = stride
        self.buffer = []

    def update(self):
        pass

    def get_buffer(self):
        return self._buffer_manager.get_buffer(stride=self._stride)

    buffer = Leaf(list[tuple[int, float, float]], get_buffer, None)


class Buffers(ParameterTreeMixin):
    def __init__(self, device: "K2470Device", buffer_manager: BufferManager):
        self._device = device
        self._buffer_manager = buffer_manager

        self.buffers = {}
        for buffer_config in self._device._config["buffers"]:
            self.buffers[buffer_config["name"]] = Buffer(
                buffer_manager,
                buffer_config["stride"],
            )

    def as_tree(self) -> ParameterTree:
        logging.info(f"{self.buffers}")
        return ParameterTree(
            {name: buffer.as_tree() for name, buffer in self.buffers.items()}
        )

    def update(self):
        for _, buffer in self.buffers.items():
            buffer.update()
