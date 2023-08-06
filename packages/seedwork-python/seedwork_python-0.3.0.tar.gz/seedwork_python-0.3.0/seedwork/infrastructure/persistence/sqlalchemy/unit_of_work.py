from traceback import TracebackException
from typing import Optional

from sqlalchemy.orm import Session, sessionmaker
from typing_extensions import Self

__all__ = ['SQLAlchemyUnitOfWork']


class SQLAlchemyUnitOfWork:
    """SQLAlchemy unit of work implementation."""

    def __init__(self, session_factory: sessionmaker) -> None:
        self.session_factory: sessionmaker = session_factory

    def commit(self) -> None:
        self._commit()

    def rollback(self) -> None:
        self._rollback()

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: TracebackException,
    ) -> None:
        self.session.rollback()
        self.session.close()

    def _commit(self) -> None:
        self.session.commit()

    def _rollback(self) -> None:
        self.session.rollback()
