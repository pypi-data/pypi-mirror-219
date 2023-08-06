"""
Documentar.
"""

from typing import Any, Union, List, Dict
from rds.core.cache import MISSING_KEY, DEFAULT_TTL


class BaseCache:
    def __init__(self, **params: Dict[str, Any]) -> None:
        self.default_ttl = int(str(params.get("ttl", DEFAULT_TTL)))

    def get_ttl(self, ttl: Union[int, None] = None) -> int:
        return ttl if (isinstance(ttl, int) and ttl >= 0) or (ttl is not None) else self.default_ttl

    def key_exists(self, key: str) -> bool:
        return self.get(key) is not MISSING_KEY

    def add(self, key: str, value: Any, ttl: Union[int, None] = None) -> bool:
        """Define um valor no cache caso a chave ainda não exista.

        Caso já exista, não define o valor no cache, preservando o TTL.

        Args:
            key (_type_): A chave a ser usada para identificar o valor no cache.
            value (_type_): O valor a ser posto em cache.
            ttl (_type_, optional): O tempo máximo que o item pode existir no cache. O padrão é None.

        Raises:
            NotImplementedError: _description_

        Returns:
            bool: True adicionou, ou seja, se ainda não existia. False se já existia.
        """
        raise NotImplementedError("subclasses of BaseCache must provide an add() method")

    def get(self, key: str, default: Any = None) -> Any:
        """Busca uma determinada chave no cache. Se a chave não existir, retorne o padrão, que por padrão é None.
        Args:
            key (_type_): A chave a ser usada para identificar o valor no cache.
            default (_type_): O valor padrão, caso não seja encontrado no cache. O padrão é None.
        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("subclasses of BaseCache must provide a get() method")

    def set(self, key: str, value: Any, ttl: Union[int, None] = None) -> None:
        """Set a value in the cache. If ttl is given, use that ttl for the key; otherwise use the default cache ttl."""
        raise NotImplementedError("subclasses of BaseCache must provide a set() method")

    def get_or_set(self, key: str, default: Any, ttl: Union[int, None] = None) -> Any:
        """Fetch a given key from the cache. If the key does not exist,
        set the key and set it to the default value. The default value can
        also be any callable. If ttl is given, use that ttl for the
        key; otherwise use the default cache ttl.

        Return the value of the key stored or retrieved.
        """
        val = self.get(key)
        if val is None:
            self.set(key, default, ttl=ttl)
            val = default
        return val

    def delete(self, key: str) -> None:
        """Delete a key from the cache and return whether it succeeded, failing silently."""
        raise NotImplementedError("subclasses of BaseCache must provide a delete() method")

    def touch(self, key: str, ttl: Union[int, None] = None) -> bool:
        """
        Update the key's expiry time using ttl. Return True if successful or False if the key does not exist.
        """
        raise NotImplementedError("subclasses of BaseCache must provide a touch() method")

    def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Fetch a bunch of keys from the cache. For certain backends (memcached, pgsql) this can be *much* faster
        when fetching multiple values.

        Return a dict mapping each key in keys to its value. If the given key is missing, it will be missing from
        the response dict.
        """
        d = {}
        for k in keys:
            val = self.get(k, MISSING_KEY)
            if val is not MISSING_KEY:
                d[k] = val
        return d

    def set_many(self, data: Any, ttl: Union[int, None] = None) -> None:
        """Set a bunch of values in the cache at once from a dict of key/value
        pairs.  For certain backends (memcached), this is much more efficient
        than calling set() multiple times.

        If ttl is given, use that ttl for the key; otherwise use the
        default cache ttl.
        """
        for key, value in data.items():
            self.set(key, value, ttl=ttl)

    def delete_many(self, keys: List[str]) -> None:
        """Delete a bunch of values in the cache at once. For certain backends
        (memcached), this is much more efficient than calling delete() multiple times.
        """
        for key in keys:
            self.delete(key)

    def incr(self, key: str, delta: Union[int, float] = 1) -> Union[int, float]:
        """NOT SAFE FOR CONCURRENCY. Add delta to value in the cache.
        If the key does not exist, raise a ValueError exception.
        """
        value = self.get(key, None)
        if value is None:
            raise ValueError("Key '%s' not found" % key)
        new_value = value + delta
        self.set(key, new_value)
        return new_value

    def decr(self, key: str, delta: Union[int, float] = 1) -> Union[int, float]:
        """NOT SAFE FOR CONCURRENCY. Subtract delta from value in the cache.
        If the key does not exist, raise a ValueError exception.
        """
        return self.incr(key, -delta)

    def clear(self) -> None:
        """Remove *all* values from the cache at once."""
        raise NotImplementedError("subclasses of BaseCache must provide a clear() method")

    def close(self, **kwargs: Dict[str, Any]) -> None:
        """Close the cache connection"""
        pass
