"""
Documentar.
"""

from typing import Any, List, Dict, Union
from rds.core.cache.base import BaseCache


class NoCache(BaseCache):
    def __init__(self, *args: List, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)

    def add(self, key: str, value: Any, ttl: Union[int, None] = None) -> bool:
        return True

    def get(self, key: str, default: Any = None) -> Any:
        return default

    def set(self, key: str, value: Any, ttl: Union[int, None] = None) -> None:
        return

    def delete(self, key: str) -> None:
        return

    def clear(self) -> None:
        return

    def key_exists(self, key: str) -> bool:
        return False
