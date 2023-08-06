from typing import Any, Protocol

__all__ = ['Cache']


class Cache(Protocol):
    """Cache client interface."""

    def get(self, key: str) -> Any:
        """Get value by given key.""" ""

    def set(self, key: str, value: Any) -> None:
        """Set key-value pair."""
