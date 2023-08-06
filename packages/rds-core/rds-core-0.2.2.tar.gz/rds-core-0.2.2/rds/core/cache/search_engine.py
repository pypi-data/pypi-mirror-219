"""
Documentar.
"""

from typing import Any, List, Dict, Union

from rds.core.cache.base import BaseCache
from rds.core.searchengine import search_engine as search_engine_func


class SearchEngineCache(BaseCache):
    def __init__(self, **params: Dict[str, Any]) -> None:
        super(SearchEngineCache, self).__init__(**params)
        self.search_engine_alias: str = str(params.get("search_engine_alias", "default"))
        self.index_name: str = str(params.get("index_name", "cnes_establecimento_cache"))
        self.refresh: str = str(params.get("refresh", "wait_for"))

    @property
    def search_engine(self) -> Any:
        return search_engine_func(self.search_engine_alias)

    def key_exists(self, key: str) -> bool:
        return self.search_engine.exists(self.index_name, id=key)

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
        if self.key_exists(key):
            return False
        body = {"value": value, "ttl": self.get_ttl(ttl)}
        self.search_engine.create(self.index_name, body=body, id=key, refresh=self.refresh)
        return True

    def get(self, key: str, default: Any = None) -> Any:
        try:
            response = self.search_engine.get(self.index_name, key)
            doc = response["_source"]
            # ttl = doc['ttl']
            return doc["value"] if doc["value"] is not None else default
        except Exception as e:
            if str(type(e))[-15:-2] == "NotFoundError":
                return default
            raise e

    def set(self, key: str, value: Any, ttl: Union[int, None] = None) -> None:
        if type(value) == bytes:
            raise ValueError("Não suporta salvar bytes")
        body = {"value": value, "ttl": self.get_ttl(ttl)}
        self.search_engine.index(self.index_name, body=body, id=key, refresh=self.refresh)

    def touch(self, key: str, ttl: Union[int, None] = None) -> bool:
        if self.key_exists(key):
            self.search_engine.index(self.index_name, body={"ttl": self.get_ttl(ttl)}, id=key, refresh=self.refresh)
            return True
        return False

    def delete(self, key: str) -> None:
        try:
            self.search_engine.delete(self.index_name, id=key, refresh=self.refresh)
        except Exception as e:
            if str(type(e))[-15:-2] == "NotFoundError":
                return None
            raise e

    def clear(self) -> None:
        raise NotImplementedError("subclasses of BaseCache must provide a clear() method")

    def get_many(self, keys: List[str]) -> Dict[str, Any]:
        """Fetch a bunch of keys from the cache. For certain backends (memcached, pgsql) this can be *much* faster
        when fetching multiple values.

        Return a dict mapping each key in keys to its value. If the given key is missing, it will be missing from
        the response dict.
        """
        response = self.search_engine.mget({"ids": [k for k in keys]}, index=self.index_name)
        return {x["_id"]: x["_source"]["value"] for x in response["docs"] if x["found"]}
