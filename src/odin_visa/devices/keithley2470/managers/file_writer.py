import h5py
import hdf5plugin
import structlog
from numpy.typing import NDArray

from odin_visa.devices.device_config import CompressionConfig, DeviceConfig
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class FileWriter:
    def __init__(self, state: K2470State, config: DeviceConfig) -> None:
        self.state = state.config
        self.config = config.savefile_config

    def create_file(self) -> None:
        path = self.state.savefile.path()
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file():
            logger.warning("File already exists", path=path)
            return

        with h5py.File(path, "w") as f:
            f.create_dataset(
                "measurements",
                shape=(0,),
                maxshape=(None,),
                dtype="f8",
                compression=self._compression_from_config(
                    self.config.measurements_compression
                ),
            )
            f.create_dataset(
                "timestamps",
                shape=(0,),
                maxshape=(None,),
                dtype="i8",
                compression=self._compression_from_config(
                    self.config.timestamp_compression
                ),
            )
        self.write_metadata()

    def write_metadata(self) -> None:
        with h5py.File(self.state.savefile.path(), "a") as f:
            try:
                grp = f.create_group("metadata")

                source_grp = grp.create_group("source")
                source_grp.attrs["delay"] = self.state.source.delay
                source_grp.attrs["auto_delay"] = self.state.source.auto_delay
                source_grp.attrs["high_capacitance"] = (
                    self.state.source.high_capacitance
                )
                source_grp.attrs["level"] = self.state.source.level
                source_grp.attrs["limit"] = self.state.source.limit
                source_grp.attrs["function"] = str(self.state.source.function)
                source_grp.attrs["protection_level"] = str(self.state.source.protection)
                source_grp.attrs["range"] = self.state.source.range
                source_grp.attrs["auto_range"] = self.state.source.auto_range
                source_grp.attrs["read_back"] = self.state.source.read_back

                sense_grp = grp.create_group("sense")
                sense_grp.attrs["averaging_enabled"] = self.state.sense.averaging
                sense_grp.attrs["averaging_count"] = self.state.sense.averaging_count
                sense_grp.attrs["averaging_type"] = str(self.state.sense.averaging_type)
                sense_grp.attrs["auto_zero"] = self.state.sense.auto_zero
                sense_grp.attrs["nplcs"] = self.state.sense.nplcs
                sense_grp.attrs["offset_compensation"] = (
                    self.state.sense.offset_compensation
                )
                sense_grp.attrs["auto_range"] = self.state.sense.auto_range
                sense_grp.attrs["auto_range_lower_limit"] = (
                    self.state.sense.auto_range_lower_limit
                )
                sense_grp.attrs["auto_range_upper_limit"] = (
                    self.state.sense.auto_range_upper_limit
                )
                sense_grp.attrs["auto_range_rebound"] = (
                    self.state.sense.auto_range_rebound
                )
                sense_grp.attrs["range"] = self.state.sense.range
                sense_grp.attrs["relative_offset"] = self.state.sense.relative_offset
                sense_grp.attrs["relative_offset_level"] = (
                    self.state.sense.relative_offset_level
                )
                sense_grp.attrs["remote_sensing"] = self.state.sense.remote_sensing
                sense_grp.attrs["count"] = self.state.sense.count
                sense_grp.attrs["function"] = str(self.state.sense.function)

                output_grp = grp.create_group("output")
                output_grp.attrs["smode"] = str(self.state.output.smode)
                output_grp.attrs["interlock"] = self.state.output.interlock
                output_grp.attrs["terminals"] = str(self.state.output.terminals)
            except Exception:
                logger.exception("Failed to write metadata")

    def write_chunk(self, chunk: NDArray) -> None:
        with h5py.File(self.state.savefile.path(), "a") as f:
            ds = f["measurements"]
            if not isinstance(ds, h5py.Dataset):
                logger.error(
                    "Could not access measurements dataset",
                    path=self.state.savefile.path,
                )
                return

            old_len = ds.shape[0]
            ds.resize(old_len + len(chunk), axis=0)
            ds[old_len:] = chunk["reading"]

            ds = f["timestamps"]
            if not isinstance(ds, h5py.Dataset):
                logger.error(
                    "Could not access measurements dataset",
                    path=self.state.savefile.path,
                )
                return

            old_len = ds.shape[0]
            ds.resize(old_len + len(chunk), axis=0)
            ds[old_len:] = chunk["timestamp"]

    def read(self) -> None:
        with h5py.File(self.state.savefile.path(), "r") as f:
            ds = f["measurements"]
            if not isinstance(ds, h5py.Dataset):
                logger.error(
                    "Could not access 'measurements' dataset",
                    path=self.state.savefile.path(),
                )
                return

    def _compression_from_config(
        self, config: CompressionConfig
    ) -> h5py.filters.FilterRefBase | None:
        match config.type:
            case "none":
                return None
            case "gzip" | "lzf" | "szip":
                return config.type
            case "blosc2":
                if config.settings is None:
                    return None
                return hdf5plugin.Blosc2(
                    cname=config.settings.cname,
                    clevel=config.settings.clevel,
                    filters=config.settings.filter.tofilter(),
                )
