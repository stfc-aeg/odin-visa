from enum import Enum


class StrEnum(str, Enum):
    """Backport of Python 3.11+ StrEnum for compatibility with older runtimes.

    Members inherit from str, so enum values can be used directly in string
    interpolation and f-strings without explicit conversion.
    """

    def __str__(self) -> str:
        return str(self.value)
