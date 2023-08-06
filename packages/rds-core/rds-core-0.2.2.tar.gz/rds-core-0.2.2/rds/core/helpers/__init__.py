"""
Documentar.
"""
from typing import Any, List, Dict
import logging
import json
from os import getenv
import importlib


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def str2bool(v):
    TRUE_STRS = ("true", "verdade", "yes", "sim", "t", "v", "y", "s", "1")
    FALSE_STRS = ("false", "falso", "no", "nao", "não", "f", "n", "0")

    if isinstance(v, bool):
        return v

    if v is None or (isinstance(v, str) and v.strip() == ""):
        return None

    if isinstance(v, int) and v in (1, 0):
        return v == 1

    if isinstance(v, str) and v.strip().lower() in TRUE_STRS + FALSE_STRS:
        return v.lower() in TRUE_STRS

    raise ValueError("Boolean value expected.")


def env(name, default=None, wrapped=False):
    result = getenv(name, default)
    if (
        wrapped
        and isinstance(result, str)
        and result[0:1] == "'"
        and result[-1:] == "'"
    ):
        return result[1:-1]
    return result


def env_as_list(name, default="", delimiter=",", wrapped=False):
    result = env(name, default, wrapped)
    if result is None:
        return None
    if type(result) == str:
        if result.strip() == "" and default.strip() == "":
            return []
        return result.split(delimiter)
    if type(result) in (list, tuple):
        return list(result)
    raise TypeError("env_as_list requires str, list or tuple as default")


def env_as_list_of_maps(name, key, default="", delimiter=",", wrapped=False):
    return [{key: x} for x in env_as_list(name, default, delimiter, wrapped)]


def env_as_bool(name, default=None, wrapped=False):
    return str2bool(env(name, default, wrapped))


def env_from_json(key, default="", wrapped=False):
    result = env(key, default, wrapped)
    return json.loads(result) if result is not None else result


def env_as_int(key, default=None, wrapped=False):
    result = env(key, default, wrapped)
    return int(result) if result is not None else result


def get_class(full_class_name: str) -> Any:
    module_name, class_name = full_class_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def instantiate_class(
    full_class_name: str, *args: List, **kwargs: Dict[str, Any]
) -> Any:
    Klass = get_class(full_class_name)
    return Klass(*args, **kwargs)


def get_variable_by_pathname(full_class_name: str) -> Any:
    module_name, class_name = full_class_name.rsplit(".", 1)
    return getattr(importlib.import_module(module_name), class_name)


def get_dict_by_pathname(obj: dict, ref: str) -> Any:
    """
    Use MongoDB style 'something.by.dot' syntax to retrieve objects from Python dicts.

    Usage:
       >>> x = {"top": {"middle" : {"nested": "value"}}}
       >>> q = 'top.middle.nested'
       >>> get_dict_by_pathname(x,q)
       "value"

    Credit: https://gist.github.com/mittenchops/5664038
    """
    val = obj
    tmp = ref
    ref = tmp.replace(".XX", "[0]")
    if tmp != ref:
        logger.warning("Warning: replaced '.XX' with [0]-th index")
    for key in ref.split("."):
        idstart = key.find("[")
        embedslist = 1 if idstart > 0 else 0
        if embedslist:
            idx = int(key[idstart + 1 : key.find("]")])
            kyx = key[:idstart]
            try:
                val = val[kyx][idx]
            except IndexError:
                logger.warning(f"Index: x['{kyx}'][{idx}] does not exist.")
                raise
        else:
            val = val.get(key, None) if val is not None else None
    return val
