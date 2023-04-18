from typing import Any, Dict, List

from requests import Response

from .api_client.open_data_discovery_ingestion_api import ODDApiClient
from .models import (
    DataEntityList,
    DataSet,
    DataSource,
    DataSourceList,
    MetadataExtension,
)


class OddIntegrator:
    source_name = "internal_host"
    service_name = "internal_service"

    def __init__(self, odd_platform_url: str, odd_collector_token: str):
        self.odd_collector_token = odd_collector_token
        self.platform_client = ODDApiClient(base_url=odd_platform_url)

    @property
    def source_oddrn(self) -> str:
        return f"//{self.service_name}/{self.source_name}"

    def register_source(self) -> int:
        reg_source_data = DataSourceList(
            items=[
                DataSource(
                    oddrn=self.source_oddrn, name=self.source_name, description=None
                )
            ]
        )
        reg_headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.odd_collector_token}",
        }

        resp: Response = self.platform_client.create_data_source(
            data=reg_source_data, headers=reg_headers
        )
        return resp.status_code

    @staticmethod
    def create_metadata_extension_list(
        metadata: Dict[str, Any],
        schema_url: str = "https://raw.githubusercontent.com/opendatadiscovery/",
    ) -> List[MetadataExtension]:
        return [
            MetadataExtension(
                schema_url=schema_url,
                metadata={key: value for key, value in metadata.items()},
            )
        ]

    def send_data_entity(self, dataset: DataSet) -> int:
        odd_request = DataEntityList(
            items=[dataset], data_source_oddrn=self.source_oddrn
        )
        resp = self.platform_client.post_data_entity_list(odd_request)
        return resp
