from dataclasses import dataclass

__all__ = ['ValueObject']


@dataclass(frozen=True)
class ValueObject:
    ...
