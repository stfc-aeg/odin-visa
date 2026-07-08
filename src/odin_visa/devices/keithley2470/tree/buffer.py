import pandas as pd
import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State, ResampleMethod

logger = structlog.get_logger()


class BufferTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.buffer
        self.driver = driver.buffer
        self.tree = AsyncParameterTree(
            {
                "range": (lambda: self.state.range, self._set_range),
                "downsample": (
                    lambda: str(self.state.downsample),
                    self._set_downsample,
                ),
                "bin_size": (lambda: self.state.bin_size, self._set_bin_size),
                "buffer": (self._get_buffer, None),
            }
        )

    def _set_range(self, value: int) -> None:
        self.state.range = value

    def _set_downsample(self, value: ResampleMethod) -> None:
        self.state.downsample = value

    def _set_bin_size(self, value: str) -> None:
        self.state.bin_size = value

    def _get_buffer(self) -> list[tuple[float, float]]:
        if self.state.buffer is None:
            return []

        start = pd.to_timedelta(self.state.range, unit="s")
        df = self.state.buffer
        df = df.loc[df.index.max() - start :]
        if (
            self.state.downsample != ResampleMethod.Full
            and self.state.bin_size is not None
        ):
            logger.info("DOWNSAMPLING")
            df = df.ffill().resample(self.state.bin_size)
        match self.state.downsample:
            case ResampleMethod.Mean:
                df = df.mean()
            case ResampleMethod.Median:
                df = df.median()
            case ResampleMethod.Min:
                df = df.min()
            case ResampleMethod.Max:
                df = df.max()
            case ResampleMethod.First:
                df = df.first()

        return [
            (int(idx.value) / 1000, rdg)
            for idx, rdg in df.ffill().itertuples(index=True, name=None)
        ]
