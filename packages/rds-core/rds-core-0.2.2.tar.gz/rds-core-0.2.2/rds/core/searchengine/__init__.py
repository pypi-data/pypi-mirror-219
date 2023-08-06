"""
Documentar.
"""

import datetime
from typing import Dict, Union, Any, List
from dynaconf.utils.boxing import DynaBox
from rds.core.config import settings
from rds.core.helpers import instantiate_class


__search_engine_cache: Dict[str, Any] = {}


def get_search_engine_config(alias: str = "default") -> DynaBox:
    return settings.SEARCH_ENGINES[alias]


def search_engine(
    alias: str = "default",
    username: Union[str, None] = None,
    password: Union[str, None] = None,
):
    se_config = get_search_engine_config(alias)

    engine = se_config["engine"]
    params = {k: v for k, v in se_config.items() if k not in ("username", "password", "engine", "dsl_engine", "hosts")}
    username = username if username else se_config["username"]
    password = password if password else se_config["password"]
    params["http_auth"] = (username, password)
    client = instantiate_class(engine, se_config["hosts"].split(","), **params)
    __search_engine_cache[alias] = client
    return client


def create_index_if_not_exists(
    index: str,
    body: Union[dict, None] = None,
    params: Union[Dict[str, Any], None] = None,
    headers: Union[Dict[str, Any], None] = None,
    alias: str = "default",
) -> bool:
    """Cria um índice caso não exista. Retorna True se criou e False se não criou.

    Args:
        index (str): nome do índice a ser criado
        body (dict|None): corpo do índice
        params (dict|None): parametros
        headers (dict|None): cabeçalhos
        alias (str): alias para o search engine

    Raises:
        exception: Erro conforme retornado pelo Search Engine.

    Returns:
        bool: True se criou. False se não criou.
    """
    if not body:
        body = {}
    try:
        search_engine(alias).indices.create(index, body=body, params=params, headers=headers)  # type: ignore
        return True
    except Exception as e:
        if getattr(e, "error", None) == "resource_already_exists_exception":
            return False
        raise e


def delete_index_if_exists(
    index_name: str,
    params: Union[Dict[str, Any], None] = None,
    headers: Union[Dict[str, Any], None] = None,
    alias: str = "default",
    fail: bool = False,
) -> bool:
    """Apaga um índice caso exista. Retorna True se apagou e False se não apagou.

    Args:
        index_name (str): nome do índice a ser criado
        params (Dict[str, Any] | None):
        headers (Dict[str, Any] | None): Union[Dict[str, Any], None] = None,
        alias (str): alias para o search engine

    Raises:
        Exception: Erro conforme retornado pelo Search Engine.

    Returns:
        bool: True se criou. False se não criou.
    """
    try:
        search_engine(alias).indices.delete(index_name, params=params, headers=headers)  # type: ignore
        return True
    except Exception as e:
        if getattr(e, "error", None) == "index_not_found_exception":
            return False
        raise Exception(e)


def query(
    index_name: str,
    query_string: Union[str, int, float, datetime.date, datetime.datetime],
    fields: Union[List, None] = None,
    alias: str = "default",
    username: Union[str, None] = None,
    password: Union[str, None] = None,
) -> Any:
    if fields is None:
        fields = []
    response = search_engine(alias, username, password).search(
        index=index_name,
        body={
            "query": {"multi_match": {"query": query_string, "fields": fields}},
        },
    )
    return response["hits"]["hits"], response["hits"]["total"]["value"]


class ToManyHits(Exception):
    pass


def get_by_term(
    index_name: str,
    term: str,
    term_value: Union[str, int, float, datetime.date, datetime.datetime],
    fields: Union[List, None] = None,
    alias: str = "default",
    username: Union[str, None] = None,
    password: Union[str, None] = None,
) -> Any:
    if fields is None:
        fields = []
    response = search_engine(alias, username, password).search(
        index=index_name,
        body={"query": {"term": {term: term_value}}},
    )
    if response["hits"]["total"]["value"] != 1:
        raise ToManyHits()
    return response["hits"]["hits"][0]


def getsource_by_term(
    index_name: str,
    term: str,
    term_value: Union[str, int, float, datetime.date, datetime.datetime],
    fields: Union[List, None] = None,
    alias: str = "default",
    username: Union[str, None] = None,
    password: Union[str, None] = None,
) -> Any:
    response = get_by_term(index_name, term, term_value, fields, alias, username, password)
    return response["_source"]


def search(
    index_name: str,
    body: dict,
    alias: str = "default",
    username: Union[str, None] = None,
    password: Union[str, None] = None,
) -> Any:
    response = search_engine(alias, username, password).search(index=index_name, body=body)
    return response["hits"]["hits"], response["hits"]["total"]["value"]


def index(
    index_name: str,
    body: Union[dict, None] = None,
    id: Any = None,
    params: Union[Dict[str, Any], None] = None,
    headers: Union[Dict[str, Any], None] = None,
    alias: str = "default",
) -> Union[Any, Any]:
    if not body:
        body = {}
    return search_engine(alias).index(
        index=index_name,
        body=body,
        id=id,
        params=params,
        headers=headers,
    )  # type: ignore


def search_engine_healthy(
    params: Union[Dict[str, Any], None] = None,
    headers: Union[Dict[str, Any], None] = None,
    alias: str = "default",
) -> bool:
    return search_engine(alias).ping(params=params, headers=headers)
