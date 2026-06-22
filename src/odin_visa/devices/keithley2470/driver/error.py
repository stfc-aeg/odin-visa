from odin_visa.devices.device import DeviceError


class InvalidResponseError(DeviceError):
    def __init__(self, response: str) -> None:
        super().__init__(f"Device gave an invalid response: '{response}'")
