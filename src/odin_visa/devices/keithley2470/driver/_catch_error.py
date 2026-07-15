from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar

import structlog

from odin_visa.devices.keithley2470.state import EventLogState
from odin_visa.devices.keithley2470.transport import DeviceMiscError

logger = structlog.get_logger()


class _HasEventLog(Protocol):
    event_log: EventLogState


Self = TypeVar("Self", bound=_HasEventLog)
R = TypeVar("R")
P = ParamSpec("P")


def catch_error(
    f: Callable[Concatenate[Self, P], Awaitable[R | None]],
) -> Callable[Concatenate[Self, P], Awaitable[R | None]]:
    @wraps(f)
    async def wrapper(self: Self, *args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return await f(self, *args, **kwargs)
        except DeviceMiscError as errors:
            logger.error(
                "Device returned errors, appending to event log.", errors=errors
            )
            for error in errors.messages:
                self.event_log.append(error)

    return wrapper
