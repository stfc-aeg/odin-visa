# ruff: noqa: ANN001, ANN002, ANN003, ANN401, ANN201, ANN202

from __future__ import annotations

import inspect
from functools import wraps
from timeit import default_timer
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import structlog


def _has_overridden_repr(value: Any) -> bool:
    return type(value).__repr__ is not object.__repr__


def _bound_arg_fields(
    func,
    args,
    kwargs,
    skip: set[str] | None = None,
) -> dict[str, str]:
    bound = inspect.signature(func).bind(*args, **kwargs)
    bound.apply_defaults()
    excluded = {"self", "cls"} | (skip or set())
    return {
        f"arg_{name}": str(value)
        for name, value in bound.arguments.items()
        if name not in excluded and _has_overridden_repr(value)
    }


def _exit_fields(result: Any, duration_s: float) -> dict[str, Any]:
    fields: dict[str, Any] = {"duration_us": duration_s * 1_000_000}
    if result is not None:
        fields["return_value"] = result
    return fields


def instrument(
    logger: structlog.stdlib.BoundLogger,
    *,
    skip: set[str] | None = None,
    fields: dict[str, Any] | None = None,
    ret: bool = True,
):
    extra = fields or {}

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log = logger.bind(
                _instrument=True, **_bound_arg_fields(func, args, kwargs, skip), **extra
            )

            log.debug("%s.enter", func.__qualname__)

            start = default_timer()
            result = func(*args, **kwargs) if ret else None
            duration_s = default_timer() - start

            log.debug("%s.exit", func.__qualname__, **_exit_fields(result, duration_s))

            return result

        return wrapper

    return decorator


def instrument_async(
    logger: structlog.stdlib.BoundLogger,
    *,
    skip: set[str] | None = None,
    fields: dict[str, Any] | None = None,
    ret: bool = True,
):
    extra = fields or {}

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            log = logger.bind(
                _instrument=True, **_bound_arg_fields(func, args, kwargs, skip), **extra
            )

            log.debug("%s.enter", func.__qualname__)

            start = default_timer()
            result = await func(*args, **kwargs) if ret else None
            duration_s = default_timer() - start

            log.debug("%s.exit", func.__qualname__, **_exit_fields(result, duration_s))

            return result

        return wrapper

    return decorator
