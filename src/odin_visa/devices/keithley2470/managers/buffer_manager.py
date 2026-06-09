from concurrent.futures import ThreadPoolExecutor
import logging
import threading
import time
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray
import pandas as pd
from tornado.concurrent import run_on_executor

from odin_visa.devices.keithley2470.config.buffer import BufferConfig
from odin_visa.devices.keithley2470.managers import ITEM_DTYPE
from odin_visa.devices.keithley2470.managers.savefile_manager import SaveFileManager
from odin_visa.types import parse_int

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


def us(td: int | None) -> pd.Timedelta | None:
    if td is None:
        return None
    return pd.to_timedelta(td, unit="us")


class BufferManager:
    def __init__(
        self,
        device: "K2470Device",
        config: BufferConfig,
    ):
        self.reader = DeviceBufferReader(device, config)
        self.savefile_manager = SaveFileManager(device)
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._stop_event = threading.Event()
        self._update_future = None
        self._config = config

        self.dataframe_cache = None
        self.is_acquiring = False
        self.acquisition_start_time = 0

    def start_acquisition(self):
        self.reader.reset()
        self.savefile_manager.create_dataset()
        self._stop_event.clear()
        self.is_acquiring = True
        self.acquisition_start_time = time.time_ns() // 1_000  # time in microseconds
        self._update_future = self.update_buffer()

    def stop_acquisition(self):
        self.is_acquiring = False
        self.savefile_manager.cleanup()
        self._stop_event.set()

    def cleanup(self):
        self.stop_acquisition()
        self.executor.shutdown(wait=False, cancel_futures=True)

    # TODO: play/pause?

    def get_buffer(
        self,
        start: int | None = None,
        end: int | None = None,
        bin_size: str | None = None,
        resample_method: str | None = None,
    ) -> list:
        df = self.get_dataframe()
        if df is None:
            return []

        if bin_size is not None:
            df = df.ffill().resample(bin_size)
        match resample_method:
            case "mean":
                df = df.mean()
            case "median":
                df = df.median()
            case "min":
                df = df.min()
            case "max":
                df = df.max()
            case "first":
                df = df.first()

        df = df.loc[us(start) : us(end)]

        arr = [
            (int(idx.value / 1000), src, rdg)
            for idx, src, rdg in df.itertuples(index=True, name=None)
        ]
        return arr

    def get_dataframe(self):
        if self.dataframe_cache is not None:
            return self.dataframe_cache

        buffer = self.savefile_manager.read()
        if buffer is None:
            return
        return pd.DataFrame(data=buffer, columns=["source", "reading"]).set_index(
            pd.to_timedelta(buffer["timestamp"], unit="us")
        )

    def invalidate_dataframe(self):
        self.dataframe_cache = None

    @run_on_executor
    def update_buffer(self):
        while self.is_acquiring and not self._stop_event.is_set():
            try:
                chunk = self.reader.read_new_items()
                if self._stop_event.is_set():
                    break
                logging.warning(f"CHUNK: {chunk}")
                self.savefile_manager.save_chunk(chunk)
            except Exception:
                if self._stop_event.is_set():
                    break
                logging.exception("Error updating device buffer")
            self._stop_event.wait(0.1)


class DeviceBufferReader:
    def __init__(self, device: "K2470Device", config: BufferConfig):
        self.device = device
        self.config = config
        self.prev_end = 0

    def reset(self):
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
        end = end % size

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
        items[::3] *= 1_000_000
        rows = items.reshape(-1, 3)
        out = np.empty(rows.shape[0], dtype=ITEM_DTYPE)
        out["timestamp"] = rows[:, 0].astype(np.int64)
        out["reading"] = rows[:, 1]
        out["source"] = rows[:, 2]

        return out
