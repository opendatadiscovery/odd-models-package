import os
from functools import wraps
from typing import Any, Optional

from odd_models.api_client.open_data_discovery_ingestion_api import ODDApiClient
from odd_models.models import (
    CompactDataEntityList,
    DataEntityList,
    DataSource,
    DataSourceList,
)
from requests import HTTPError

from .errors import (
    CreateDataSourceError,
    CreateTokenError,
    EmptyHostError,
    EmptyTokenError,
    GetDegChildrenError,
    IngestionEntitiesError,
)


def provide_token(method):
    @wraps(method)
    def inner(*args, **kwargs):
        client: Client = args[0]
        if client._token is None:
            raise EmptyTokenError()

        headers = kwargs.get("headers") or {}
        headers["Authorization"] = f"Bearer {client._token}"
        kwargs["headers"] = headers

        return method(*args, **kwargs)

    return inner


def with_header(name: str, value: str):
    def wrapper(method):
        @wraps(method)
        def wrapped(*args, **kwargs):
            headers = kwargs.get("headers") or {}
            headers[name] = value
            kwargs["headers"] = headers
            return method(*args, **kwargs)

        return wrapped

    return wrapper


class Client:
    create_token_endpoint = "/api/collectors"

    def __init__(self, host: str = None, token: str = None) -> None:
        self._host = host or os.getenv("ODD_PLATFORM_HOST", None)
        self._token = token or os.getenv("ODD_PLATFORM_TOKEN", None)

        if self._host is None:
            raise EmptyHostError()

        self._client = ODDApiClient(self._host)

    def auth(self, *, name: str, description: Optional[str]) -> None:
        token = self.create_token(name=name, description=description)
        self._token = token

    def get_data_entities_by_deg_oddrn(self, oddrn: str) -> CompactDataEntityList:
        headers = {"Authorization": f"Bearer {self._token}"}
        response = self._client.get_data_entities_by_deg_oddrn(
            oddrn=oddrn, headers=headers
        )

        try:
            response.raise_for_status()
            return CompactDataEntityList.parse_raw(response.json())
        except HTTPError as e:
            message = e.response.json().get("message")
            raise GetDegChildrenError(oddrn, message) from e

    def create_token(self, *, name: str, description: Optional[str]) -> str:
        """Request for creating token

        Args:
            name (str): name
            description (Optional[str]): Optional description

        Returns:
            str: created token
        """
        data = {"name": name, "description": description}
        response = self._client.post(self.create_token_endpoint, data=data)

        try:
            response.raise_for_status()
            return response.json().get("token").get("value")
        except HTTPError as e:
            message = e.response.json().get("message")
            raise CreateTokenError(message) from e

    @provide_token
    @with_header("content-type", "application/json")
    def create_data_source(
        self,
        *,
        data_source_oddrn: str,
        data_source_name: str,
        headers: dict[Any, str] = None,
    ) -> None:
        data = DataSourceList(
            items=[DataSource(oddrn=data_source_oddrn, name=data_source_name)]
        )
        response = self._client.create_data_source(data=data, headers=headers)

        try:
            response.raise_for_status()
        except HTTPError as e:
            message = e.response.json().get("message")
            raise CreateDataSourceError(
                data_source_name, data_source_oddrn, message
            ) from e

    @provide_token
    @with_header("content-type", "application/json")
    def ingest_data_entity_list(
        self, *, data_entities: DataEntityList, headers: dict[Any, str] = None
    ) -> None:
        data = data_entities
        response = self._client.post_data_entity_list(data=data, headers=headers)

        try:
            response.raise_for_status()
        except HTTPError as e:
            message = e.response.json().get("message")
            raise IngestionEntitiesError(
                data_entities.data_source_oddrn, message
            ) from e
