from typing import Protocol, TypeVar

from seedwork.domain import AggregateRoot

__all__ = ['Repository']

T = TypeVar('T', bound=AggregateRoot, covariant=True)


class Repository(Protocol[T]):
    ...
