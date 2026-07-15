from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Concatenate, ParamSpec, Protocol, TypeVar, cast

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
    f: Callable[Concatenate[Self, P], Awaitable[R]],
) -> Callable[Concatenate[Self, P], Awaitable[R]]:
    @wraps(f)
    async def wrapper(self: Self, *args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return await f(self, *args, **kwargs)
        except DeviceMiscError as e:
            logger.error("Device returned errors, appending to event log.", errors=e)
            for error in e.messages:
                self.event_log.append(error)
            raise e

    return wrapper
