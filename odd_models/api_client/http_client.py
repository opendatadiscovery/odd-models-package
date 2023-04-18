import json
import logging
from functools import wraps
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel
from requests import Response, Session

DEFAULT_API_TIMEOUT = 30


def validate_schema(schema: Type[BaseModel]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            req_data = kwargs.pop("data", None) or args[1]
            if isinstance(req_data, dict):
                obj = schema.parse_obj(req_data)
                req_data = json.loads(obj.json(exclude_none=True))
            elif isinstance(req_data, schema):
                req_data = json.loads(req_data.json(exclude_none=True))
            else:
                raise ValueError(
                    f"'data' argument must be dict or instance of model {schema}"
                )
            return func(args[0], req_data, **kwargs)

        return wrapper

    return decorator


class WrongRequestException(Exception):
    pass


class HttpClient:
    base_url = None

    def _fetch_response(
        self,
        path: str,
        method: str,
        params: Optional[Dict] = None,
        data: Optional[Any] = None,
        json: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        url = self.base_url + path

        request_data = {
            "params": params,
            "data": data,
            "json": json,
            "allow_redirects": False,
            "headers": headers or {},
            "timeout": timeout or DEFAULT_API_TIMEOUT,
        }
        try:
            session = Session()
            if method == "GET":
                response = session.get(url, **request_data)
            elif method == "POST":
                response = session.post(url, **request_data)
            elif method == "PATCH":
                response = session.patch(url, **request_data)
            elif method == "PUT":
                response = session.put(url, **request_data)
            else:
                raise WrongRequestException(f"Unsupported method type {method}")
        except Exception as e:
            logging.error("An error occurred while sending the request")
            raise
        return response

    def get(
        self,
        path: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        return self._fetch_response(
            path, method="GET", params=params, headers=headers, timeout=timeout
        )

    def post(
        self,
        path: str,
        data: Optional[Any] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        return self._fetch_response(
            path, method="POST", json=data, headers=headers, timeout=timeout
        )

    def patch(
        self,
        path: str,
        data: Optional[Any] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        return self._fetch_response(
            path, method="PATCH", json=data, headers=headers, timeout=timeout
        )

    def put(
        self,
        path: str,
        data: Optional[Any] = None,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ) -> Response:
        return self._fetch_response(
            path, method="PUT", json=data, headers=headers, timeout=timeout
        )
