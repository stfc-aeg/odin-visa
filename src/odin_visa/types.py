"""Parsing utilities and polyfills for VISA device communication.

Provides safe parsers for SCPI response strings that gracefully handle
None and malformed values by returning configurable defaults."""

from enum import Enum
from typing import List, Type, TypeVar


class StrEnum(str, Enum):
    """Backport of Python 3.11+ StrEnum for compatibility with older runtimes.

    Members inherit from str, so enum values can be used directly in string
    interpolation and f-strings without explicit conversion.
    """

    def __str__(self) -> str:
        return str(self.value)


def parse_int(raw: str | None, default: int = 0) -> int:
    """Safely parses an integer from a SCPI response string.

    Returns the default value if the input is None or cannot be parsed as an integer.

    Args:
        raw: The raw string from a SCPI query response, or None.
        default: Value to return if parsing fails. Defaults to 0.

    Returns:
        The parsed integer, or the default value.
    """
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def parse_float(raw: str | None, default: float = 0.0) -> float:
    """Safely parses a float from a SCPI response string.

    Returns the default value if the input is None or cannot be parsed as a float.

    Args:
        raw: The raw string from a SCPI query response, or None.
        default: Value to return if parsing fails. Defaults to 0.0.

    Returns:
        The parsed float, or the default value.
    """
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def parse_float_list(raw: str | None, default: List[float] = []) -> List[float]:
    """Parses a comma-separated list of floats from a SCPI response.

    Used to parse multi-value buffer responses from commands like TRAC:DATA?,
    which return comma-delimited reading values.

    Args:
        raw: Comma-separated float string, or None.
        default: Value to return if parsing fails. Defaults to [].

    Returns:
        A list of parsed floats, or the default value.
    """
    if raw is None:
        return default
    try:
        return list(map(parse_float, raw.split(",")))
    except ValueError:
        return default


def parse_bool(raw: str | None, default: bool = False) -> bool:
    """Parses a boolean-like value from a SCPI response.

    Accepts '1' and 'ON' as True, '0' and 'OFF' as False.
    Whitespace is stripped and comparison is case-insensitive.

    Args:
        raw: The raw string from a SCPI query response, or None.
        default: Value to return if parsing fails. Defaults to False.

    Returns:
        The parsed boolean, or the default value.
    """
    if raw is None:
        return default
    normalised = raw.strip().upper()
    if normalised in ("1", "ON"):
        return True
    if normalised in ("0", "OFF"):
        return False
    return default


E = TypeVar("E", bound=StrEnum)


def parse_enum(raw: str | None, enum_cls: Type[E], default: E) -> E:
    """Parses a SCPI response string into a StrEnum member.

    Matches the raw value (case-insensitive) against each enum member's
    value. Used to parse function names like 'VOLT' -> SenseFunction.VOLTAGE.

    Args:
        raw: The raw string from a SCPI query response, or None.
        enum_cls: The StrEnum subclass to match against.
        default: Enum member to return if no match is found.

    Returns:
        The matched enum member, or the default value.
    """
    if raw is None:
        return default
    normalised = raw.strip().upper()
    for member in enum_cls:
        if member.value.upper() == normalised:
            return member
    return default
