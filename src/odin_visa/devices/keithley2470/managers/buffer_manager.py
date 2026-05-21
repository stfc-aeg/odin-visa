import logging
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

from odin_visa.devices.keithley2470.config.buffer import BufferConfig
from odin_visa.types import parse_int

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


ITEM_DTYPE = np.dtype([("seconds_offset", "f8"), ("source", "f8"), ("reading", "f8")])


class BufferManager:
    def __init__(self, device: "K2470Device", config: BufferConfig):
        self.reader = DeviceBufferReader(device, config)

        self.current_buffer = np.empty(0, dtype=ITEM_DTYPE)

        self.is_acquiring = False

    def start_acquisition(self):
        self.current_buffer = np.empty(0, dtype=ITEM_DTYPE)
        self.is_acquiring = True

    def stop_acquisition(self):
        self.is_acquiring = False

    # TODO: play/pause?

    def get_buffer(self, start: int = 0, stride: int = 1) -> NDArray:
        """Get the current buffer of data, from a given start index, with a given stride (for downsampling)"""
        # get_buffer() is called with the 'downsampled local' start index
        corrected_start = int(start * stride)
        return self.current_buffer[corrected_start::stride]

    def update(self):
        if self.is_acquiring:
            self.current_buffer = np.concat(
                [self.current_buffer, self.reader.read_new_items()]
            )


class DeviceBufferReader:
    def __init__(self, device: "K2470Device", config: BufferConfig):
        self.device = device
        self.config = config
        self.prev_end = 0

    def read_new_items(self) -> NDArray:
        """Read the new items from the devices ring buffer"""

        name = self.config.name
        size = self.config.size
        start = self.prev_end % size + 1

        response = self.device.query(f':TRAC:ACT? "{name}" ; ACT:END? "{name}"')
        if response is None:
            return np.empty(0, dtype=ITEM_DTYPE)

        count, end = map(parse_int, response.split(";"))

        # no new items have been added
        if self.prev_end == end:
            logging.info("No buffer items to read")
            return np.empty(0, dtype=ITEM_DTYPE)

        # the buffer didn't wrap during this period, so all elements are contiguous
        # 001 ....!!!!!!!!!!!.... 100
        #         ^         ^
        #       start      end
        elif self.prev_end < end:
            logging.info(
                f"Reading {end - self.prev_end} buffer items from {start} to {end}"
            )
            self.prev_end = end
            return self.parse_buffer_response(
                self.device.query(
                    f':TRAC:DATA? {start}, {end}, "{name}", REL, SOUR, READ'
                )
            )

        # the buffer has wrapped this period, elements are split at the start and end of the buffer
        # 001 !!!!!!.........!!!! 100
        #          ^         ^
        #         end      start
        else:
            logging.info(
                f"Buffer wrapped, reading {(count - self.prev_end) + end} buffer items from {start} to {count} and from 1 to {end}"
            )
            self.prev_end = end
            to_buf_end = self.parse_buffer_response(
                self.device.query(
                    f':TRAC:DATA? {start}, {size}, "{name}", REL, SOUR, READ'
                )
                or ""
            )
            from_buf_start = self.parse_buffer_response(
                self.device.query(f':TRAC:DATA? 1, {end}, "{name}", REL, SOUR, READ')
                or ""
            )
            return np.concatenate([to_buf_end, from_buf_start])

    def parse_buffer_response(self, response: str | None) -> NDArray:
        """Parse the string response from the device into a NDArray[ITEM_DTYPE]"""
        if response is None:
            return np.empty(0, ITEM_DTYPE)

        # parse to array of float64s, then treat each group of 3 as single ITEM_DTYPE
        items = np.fromstring(response, sep=",")
        logging.debug(f"dtype: {ITEM_DTYPE}")
        return items.view(ITEM_DTYPE)
