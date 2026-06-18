from odin_visa.types import StrEnum
from typing import TypeVar, Type


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
    raise ValueError(f"value `{raw}` is not bool-like")


def parse_float_list(raw: str) -> list[float]:
    values: list[float] = []
    for i, part in enumerate(raw.split(",")):
        try:
            parse_float(part.strip())
        except ValueError as e:
            raise ValueError(f"Could not parse element {i} of {raw}: {e}")
    return values


E = TypeVar("E", bound=StrEnum)


def parse_enum(raw: str, enum_cls: Type[E]) -> E:
    normalised = raw.strip().upper()
    for member in enum_cls:
        if member.value.upper() == normalised:
            return member
    raise ValueError(f"Could not parse {raw} into {enum_cls}")
