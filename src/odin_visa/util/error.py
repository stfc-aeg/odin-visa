from typing import Type, TypeAlias
from dataclasses import dataclass


@dataclass(frozen=True)
class ParseListElementError:
    from_str: str
    index: int
    reason: ValueError


@dataclass(frozen=True)
class NoSuchVariantError:
    from_str: str
    into_enum: Type


ParseError: TypeAlias = ParseListElementError | NoSuchVariantError | ValueError
