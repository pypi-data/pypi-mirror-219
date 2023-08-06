import time
from typing import Any, Union, Dict
from rds.core.cache import MISSING_KEY
from rds.core.cache.base import BaseCache


class InMemoryCache(BaseCache):
    def __init__(self, **params: Dict[str, Any]):
        super().__init__(**params)
        self.clear()

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __delitem__(self, key) -> None:
        self.delete(key)

    def add(self, key: str, value: Any, ttl: Union[int, None] = None) -> bool:
        if self.key_exists(key):
            return False
        self.set(key, value, ttl)
        return True

    def set(self, key: str, value: Any, ttl: Union[int, None] = None) -> None:
        expire_time = time.time() + (ttl if ttl is not None else self.default_ttl)
        self.cache[key] = (value, expire_time)

    def get(self, key: str, default: Any = None) -> Any:
        if key not in self.cache:
            return MISSING_KEY

        value, expire_time = self.cache[key]
        if time.time() > expire_time:
            del self.cache[key]
            return MISSING_KEY

        return value or default

    def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]

    def clear(self) -> None:
        self.cache = {}

    def touch(self, key: str, ttl: Union[int, None] = None) -> bool:
        value = self.get(key)
        if value != MISSING_KEY:
            self.set(key, value, ttl)
        return value != MISSING_KEY
