import datetime as dt
import time
import uuid
from dataclasses import dataclass
from typing import Any, Iterator, List, Optional

import msgpack
from loguru import logger
from redis import StrictRedis
from redis.sentinel import Sentinel
from rediscluster import ClusterBlockingConnectionPool, RedisCluster

from seedwork.exceptions import ServiceConfigException
from seedwork.message import ExtensionMessage
from seedwork.util import datetime as datetime_util

from .cache import CacheClient

__all__ = ['RedisCacheClient']


@dataclass
class RedisCacheClient(CacheClient):
    redis_url: str
    redis_password: Optional[str]
    redis_sentinel_nodes: Optional[List[str]]
    redis_cluster_nodes: Optional[List[str]]
    redis_conn_name: Optional[str] = 'redis_default'

    def get(self, key: str) -> Any:
        value: Any = self.raw_client.get(key)
        return msgpack.unpackb(value, strict_map_key=False) if value else None

    def set(self, key: str, value: Any) -> None:
        value = self.encode(value)
        return self.raw_client.set(key, value)

    def mset(self, mapping: dict) -> None:
        with self.client.pipeline() as p:
            for key, value in mapping.items():
                value = self.encode(value)
                p.set(key, value)
            p.execute()

    @classmethod
    def encode(cls, value: Any) -> bytes:
        def encode_datetime(obj: Any):
            if isinstance(obj, dt.datetime):
                return datetime_util.datetime_format(obj)
            return obj

        value = msgpack.packb(value, default=encode_datetime)
        return value

    def exists(self, key: str) -> bool:
        return self.client.exists(key)

    def keys(self, pattern: str) -> Iterator[str]:
        return self.client.scan_iter(match=pattern)

    def add(self, key: str, *values: Any) -> Any:
        return self.client.sadd(key, *values)

    def append(self, key: str, value: Any) -> Any:
        if not isinstance(value, list):
            value = [value]

        if self.exists(key):
            old_value: list = self.get(key)
            old_value.extend(value)
            self.set(key, old_value)
        else:
            self.set(key, value)

    def delete(self, key: str) -> Any:
        self.client.delete(key)

    def acquire_lock(self, lock_name: str, acquire_time=60, time_out=60):
        """获取一个分布式锁"""
        identifier = str(uuid.uuid4())
        end = time.time() + acquire_time
        lock = f"string:lock:{lock_name}"
        while time.time() < end:
            if self.client.setnx(lock, identifier):
                # 给锁设置超时时间, 防止进程崩溃导致其他进程无法获取锁
                self.client.expire(lock, time_out)
                return identifier
            elif not self.client.ttl(lock):
                self.client.expire(lock, time_out)
            time.sleep(0.001)
        return False

    def release_lock(self, lock_name: str, identifier: str):
        """释放锁"""
        lock = f"string:lock:{lock_name}"
        pip = self.client.pipeline(True)
        while True:
            try:
                pip.watch(lock)
                lock_value = self.client.get(lock)
                if not lock_value:
                    return True
                if not isinstance(lock_value, str):
                    lock_value = lock_value.decode
                if lock_value == identifier:
                    pip.multi()
                    pip.delete(lock)
                    pip.execute()
                    return True
                pip.unwatch()
                break
            except ServiceConfigException:
                pass
        return False

    def __post_init__(self) -> None:
        connection_kwargs = dict(
            socket_timeout=0.5, retry_on_timeout=True, socket_keepalive=True
        )
        if password := self.redis_password:
            connection_kwargs['password'] = password

        if redis_cluster_nodes := self.redis_cluster_nodes:
            startup_nodes = self._get_rc_startup_nodes(redis_cluster_nodes)
            connection_pool = ClusterBlockingConnectionPool(
                startup_nodes, **connection_kwargs
            )
            self.client = RedisCluster(
                connection_pool=connection_pool, decode_responses=True
            )
            self.raw_client = RedisCluster(connection_pool=connection_pool)
        elif sentinel_nodes := self.redis_sentinel_nodes:
            sentinels = self._get_sentinel_nodes(sentinel_nodes)
            sentinel = Sentinel(sentinels, decode_responses=True, **connection_kwargs)
            raw_sentinel = Sentinel(sentinels, **connection_kwargs)
            self.client = sentinel.master_for('mymaster', **connection_kwargs)
            self.raw_client = raw_sentinel.master_for('mymaster', **connection_kwargs)
        else:
            redis_url = self.redis_url
            self.client = StrictRedis.from_url(
                redis_url, decode_responses=True, **connection_kwargs
            )
            self.raw_client = StrictRedis.from_url(redis_url, **connection_kwargs)

        logger.info(f'Initializing redis hook for conn_name {self.redis_conn_name}')
        self._detect_connectivity()

    @staticmethod
    def _get_sentinel_nodes(sentinel_nodes: List[str]) -> List[tuple]:
        start_up_nodes = list()
        for node in sentinel_nodes:
            host, port = node.split(':')
            start_up_nodes.append((host, port))
        return start_up_nodes

    @staticmethod
    def _get_rc_startup_nodes(redis_cluster_nodes: List[str]) -> List[dict]:
        start_up_nodes = list()
        for node in redis_cluster_nodes:
            host, port = node.split(':')
            start_up_nodes.append(dict(host=host, port=port))
        return start_up_nodes

    def _detect_connectivity(self):
        try:
            self.client.ping()
        except ConnectionError:
            raise ServiceConfigException(ExtensionMessage.REDIS_CONNECT_ERROR)
