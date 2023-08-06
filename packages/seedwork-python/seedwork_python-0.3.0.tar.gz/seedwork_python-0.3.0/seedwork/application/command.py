from pydantic.dataclasses import dataclass

__all__ = ['Command']


@dataclass(frozen=True)
class Command:
    ...
