import logging
from returns.result import Result, Success, Failure
from typing import TypeVar, Callable

T = TypeVar("T")


def set_or_log_error(set_function: Callable[[T], Result[None, Exception]]):
    def inner(value: T):
        match set_function(value):
            case Success(_):
                return
            case Failure(e):
                logging.error(f"Could not set parameter: {e}")
                return

    return inner
