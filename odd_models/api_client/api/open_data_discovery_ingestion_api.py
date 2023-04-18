from typing import Dict, Optional, Union

from pydantic import BaseModel

from odd_models import models
from odd_models.api_client.http_client import HttpClient, validate_schema


class ODDApiClient(HttpClient):
    base_url = None

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    @validate_schema(models.IngestionAlertList)
    def create_alerts(
        self,
        data: Union[dict, BaseModel],
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        request_data = {
            "path": "/ingestion/alerts",
            "data": data,
            "headers": headers,
            "timeout": timeout,
        }
        return self.post(**request_data)

    @validate_schema(models.DataSourceList)
    def create_data_source(
        self,
        data: Union[dict, BaseModel],
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        request_data = {
            "path": "/ingestion/datasources",
            "data": data,
            "headers": headers,
            "timeout": timeout,
        }
        return self.post(**request_data)

    def get_data_entities_by_deg_oddrn(
        self,
        oddrn,
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        request_data = {
            "path": "/ingestion/entities/degs/children",
            "params": {
                "oddrn": oddrn,
            },
            "headers": headers,
            "timeout": timeout,
        }
        return self.get(**request_data)

    @validate_schema(models.MetricSetList)
    def ingest_metrics(
        self,
        data: Union[dict, BaseModel],
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        request_data = {
            "path": "/ingestion/metrics",
            "data": data,
            "headers": headers,
            "timeout": timeout,
        }
        return self.post(**request_data)

    @validate_schema(models.DataEntityList)
    def post_data_entity_list(
        self,
        data: Union[dict, BaseModel],
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        request_data = {
            "path": "/ingestion/entities",
            "data": data,
            "headers": headers,
            "timeout": timeout,
        }
        return self.post(**request_data)

    @validate_schema(models.DatasetStatisticsList)
    def post_data_set_stats_list(
        self,
        data: Union[dict, BaseModel],
        headers: Optional[Dict] = None,
        timeout: Optional[int] = None,
    ):
        request_data = {
            "path": "/ingestion/entities/datasets/stats",
            "data": data,
            "headers": headers,
            "timeout": timeout,
        }
        return self.post(**request_data)
