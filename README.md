# odin-visa

An [ODIN Control](https://github.com/odin-detector/odin-control) adapter for VISA instruments.

## Supported Devices

- Keithley SourceMeter Model 2470

> [!IMPORTANT]
> When odin-visa successfully connects to a configured Keithley SourceMeter, it will RESET the instrument to its default settings, and clear the reading buffers (`*RST` command). This is done to ensure predictable control of the device.

## Install and Run

### Adapter

```sh
# create and activate virtual environment (if needed)
python -m venv .venv
source .venv/bin/activate

# install dependencies
python -m pip install -e .

# run odin_control with your config
odin_control --config path/to/visa.cfg
```

See [Config](#config) for the required configuration files.

### odin-react

```sh
cd react/app
npm install
cp .env.example .env.local
npm run dev
```

Set `VITE_ENDPOINT_URL` in `.env.local` to the adapter URL.

## Config

Create an ODIN Control configuration:

```ini
[server]
http_addr = 127.0.0.1
http_port = 8888
adapters = visa
enable_cors = true

[adapter.visa]
module = odin_visa.adapter.VisaAdapter
devices_config = path/to/devices.json
```

Add any devices to connect to, along with any configuration options for each device.

```jsonc
{
  "devices": [
    {
      "name": "example_device",
      "type": "K2470",
      "address": "TCPIP::192.0.2.1::INSTR"
      // optional additional device configuration options - see the complete example configuration below
    }
  ]
}
```

### Complete Example Configuration

The following configuration contains all the possible options to configure (and their default values). 

```jsonc
{
  "devices": [
    {
      "name": "example_device",
      "type": "K2470",
      "address": "TCPIP::192.0.2.1::INSTR",

      // the values to initialise the device with on connection
      "default_state": {
        "acquisition": {
          "acquiring": false
        },
        "source": {
          "delay": 0.0,
          "auto_delay": false,
          "high_capacitance": false,
          "level": 0.0,
          "limit": 0.1,
          "limit_tripped": false,
          "function": "VOLTAGE",
          "protection": "PROT20",
          "protection_tripped": false,
          "range": 2.0,
          "auto_range": false,
          "read_back": true
        },
        "sense": {
          "averaging_count": 1,
          "averaging": false,
          "averaging_type": "REPEAT",
          "auto_zero": false,
          "nplcs": 0.1,
          "offset_compensation": false,
          "auto_range": false,
          "auto_range_lower_limit": 1e-08,
          "auto_range_rebound": false,
          "auto_range_upper_limit": 0.1,
          "range": 0.1,
          "relative_offset_level": 0,
          "relative_offset": false,
          "remote_sensing": false,
          "count": 1,
          "function": "CURRENT"
        },
        "savefile": {
          "enable": true,
          "file": "YYYY-MM-DDTHHMMSSZ.hdf5",
          "subfolder": "",
          "base_folder": ""
        },
        "output": {
          "smode": "NORMAL",
          "interlock": false,
          "interlock_tripped": false,
          "enabled": false,
          "terminals": "FRONT"
        },
        "poll_freq": 1.0 // how often (in seconds) to poll the device
      },
      // the buffer on the device used for all measurements from odin-visa
      "device_buffer": {
        "name": "odin_buffer",
        "size": 50000
      },
      // options for persisting acquisitions to disk
      "savefile_config": {
        "data_folder": "/data", // base folder for all saved files
        "save_frequency": 10, // how many device 'polls' to wait per disk write
        // measurements dataset compression options
        "measurements_compression": {
          // options: "none", "blosc2", "gzip", "lzf", "szip"
          "type": "blosc2",
          // only used for "blosc2"
          "settings": {
            "filter": "shuffle",
            "clevel": 3,
            "cname": "zstd"
          }
        },
        // timestamp dataset compression options
        "timestamp_compression": {
          // options: "none", "blosc2", "gzip", "lzf", "szip"
          "type": "blosc2",
          // only used for "blosc2"
          "settings": {
            "filter": "bitshuffle",
            "clevel": 3,
            "cname": "zstd"
          }
        }
      }
    }
  ]
}
```
