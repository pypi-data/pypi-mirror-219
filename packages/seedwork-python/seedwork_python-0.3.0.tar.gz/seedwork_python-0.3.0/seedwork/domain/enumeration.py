from abc import ABCMeta
from dataclasses import dataclass
from typing import Any


@dataclass
class Enumeration(metaclass=ABCMeta):
    id: int
    name: str

    def absolute_difference(self, other: 'Enumeration') -> int:
        return abs(self.id - other.id)

    def __eq__(self, other: Any) -> bool:
        return other.__class__ is self.__class__ and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return self.name
