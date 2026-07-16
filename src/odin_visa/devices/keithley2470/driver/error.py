from odin_visa.devices.device import DeviceError


class InvalidResponseError(DeviceError):
    def __init__(self, response: str) -> None:
        super().__init__(f"Device gave an invalid response: '{response}'")


class IncorrectResponseCountError(DeviceError):
    def __init__(self, response: str, expected_count: int, actual_count: int) -> None:
        super().__init__(
            f"Device returned incorrect number of responses (expected {expected_count} but got {actual_count}): {response}"
        )


class InvalidBufferSizeError(DeviceError):
    def __init__(self, size: int) -> None:
        super().__init__(f"Device returned a buffer of an invalid size: {size}")
