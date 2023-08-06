from typing import Any, Protocol

__all__ = ['Logger']


class Logger(Protocol):
    def log(self, message: str, **kwargs: Any) -> None:
        ...
