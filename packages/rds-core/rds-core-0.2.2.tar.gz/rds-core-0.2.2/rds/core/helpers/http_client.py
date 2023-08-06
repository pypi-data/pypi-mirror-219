"""
Documentar.
"""

from typing import Dict, List, Any, Union
import json
from http.client import HTTPException as OriginalHTTPException
import requests
from requests.structures import CaseInsensitiveDict
from rds.core.config import settings

DEFAULT_HEADERS: Dict[str, Any] = settings.get("DEFAULT_HEADERS", {})


class HTTPException(OriginalHTTPException):
    def __init__(
        self,
        message: str,
        url: str,
        status_code: Union[str, None] = None,
        reason: Union[str, None] = None,
        request_headers: Union[Dict[Any, Any], None] = None,
        response_headers: Union[CaseInsensitiveDict, None] = None,
    ) -> None:
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        self.reason = reason
        self.request_headers = request_headers
        self.response_headers = response_headers


def get(url: str, headers: Dict[str, str] = {}, encoding: str = "utf-8", decode: bool = True, **kwargs) -> Any:
    _headers = {**DEFAULT_HEADERS, **headers}
    try:
        response = requests.get(url, headers=_headers, **kwargs)
    except Exception as e:
        raise e

    if response.ok:
        result = response.content.decode(encoding) if decode and encoding is not None else response.content
        return result
    else:
        message = f"{response.status_code} - {response.reason}"
        raise HTTPException(message, url, str(response.status_code), response.reason, _headers, response.headers)


def get_json(
    url: str, headers: Dict[str, str] = {}, encoding: str = "utf-8", json_kwargs: Dict[str, Any] = {}, **kwargs
) -> Union[List[Any], Dict[str, Any]]:
    content = get(url, headers=headers, encoding=encoding, **kwargs)
    return json.loads(content, **json_kwargs)
