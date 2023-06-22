from odd_models.api_client.v2.odd_api_client import Client
from odd_models.discovery.data_assets.data_asset import MappableToDataEntity
from odd_models.models.models import DataEntity, DataEntityList


class DataSource:
    """Context class for adding new DataEntities to already created data source at ODD Platform

    Attributes:
        oddrn: ODDRN for an already created data source.
        client: API client for ODD Platform. If not provided, default client will be used with arguments from ENV.
        _entities: List of DataEntities to be added to data source.

    Examples:
        from odd_models.discovery import DataSource
        from odd_models.data_assets import S3Lambda, Database, S3Artifact

        with DataSource("//aws/data_source_oddrn") as data_source:
            test_lambda = Lambda("//aws/lambdas/test")

            test_data = S3Artifact.from_url("s3://bucker/folder/test_data.csv")
            test_results = S3Artifact.from_url("s3://bucker/folder/test_results.json")

            test_data >> test_lambda
            test_lambda >> test_results

            data_source.add_entity(auth_lambda)
    """

    def __init__(self, oddrn: str, client: Client = None) -> None:
        self._oddrn: str = oddrn
        self._client: Client = client or Client()

        self._entities: list[DataEntity] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save()

    def save(self):
        data_entity_list = DataEntityList(
            data_source_oddrn=self._oddrn, items=self._entities
        )
        self._client.ingest_data_entity_list(data_entities=data_entity_list)

    def add_data_asset(self, data_asset: MappableToDataEntity):
        """Receives DataAsset maps and adds it to the list of DataEntities."""
        data_entity = data_asset.to_data_entity()
        self._entities.append(data_entity)
