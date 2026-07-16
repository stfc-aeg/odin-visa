from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class SCPIQuery(Generic[T]):
    query: str
    parser: Callable[[str], T]
