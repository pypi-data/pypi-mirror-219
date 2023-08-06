from typing import Any, Optional


class RedisClient:
    """Redis client implementation.

    This class is a wrapper around redis-py client.

    Attributes:
        redis_url: Redis connection URL.

        redis_password: Redis password.

        redis_sentinel_nodes: Redis sentinel nodes.
            If provided, redis_url will be ignored.
            Examples:
                - redis_sentinel_nodes = ['redis://localhost:63', 'redis://localhost:26380']

        redis_cluster_nodes: Redis cluster nodes.
            If provided, redis_url and redis_sentinel_nodes will be ignored.
            Examples:
                - redis_cluster_nodes = ['redis://localhost:63', 'redis://localhost:26380']

    """

    redis_url: str
    redis_password: Optional[str]
    redis_sentinel_nodes: Optional[list[str]]
    redis_cluster_nodes: Optional[list[str]]

    def __post__init__(self) -> None:
        connection_kwargs = dict(
            socket_timeout=0.5, retry_on_timeout=True, socket_keepalive=True
        )
        if password := self.redis_password:
            connection_kwargs['password'] = password

    def get(self, key: str) -> Any:
        ...

    def set(self, key: str, value: Any) -> None:
        ...
