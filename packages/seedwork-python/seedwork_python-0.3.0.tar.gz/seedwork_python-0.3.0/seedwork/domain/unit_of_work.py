from traceback import TracebackException
from typing import Optional, Protocol, runtime_checkable

from typing_extensions import Self

__all__ = ['IUnitOfWork']


@runtime_checkable
class IUnitOfWork(Protocol):
    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def __enter__(self) -> Self:
        ...

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        ...
