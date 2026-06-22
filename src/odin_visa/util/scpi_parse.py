from typing import TypeVar

from odin_visa.types import StrEnum


def parse_int(raw: str) -> int:
    return int(raw)


def parse_float(raw: str) -> float:
    return float(raw)


def parse_bool(raw: str) -> bool:
    normalised = raw.strip().upper()
    if normalised in ("1", "ON"):
        return True
    if normalised in ("0", "OFF"):
        return False

    msg = f"value `{raw}` is not bool-like"
    raise ValueError(msg)


def parse_float_list(raw: str) -> list[float]:
    values: list[float] = []
    for part in raw.split(","):
        parse_float(part.strip())
    return values


E = TypeVar("E", bound=StrEnum)


def parse_enum(raw: str, enum_cls: type[E]) -> E:
    normalised = raw.strip().upper()
    for member in enum_cls:
        if member.value.upper() == normalised:
            return member
    msg = f"Could not parse '{raw}' into {enum_cls}"
    raise ValueError(msg)
