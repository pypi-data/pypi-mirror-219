from abc import abstractmethod
from typing import Any, Protocol


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        ...
