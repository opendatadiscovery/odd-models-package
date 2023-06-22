from odd_models.discovery.data_assets.data_asset import DataAsset
from odd_models.models import DataEntity


class Database(DataAsset):
    def __init__(self, oddrn: str) -> None:
        self.oddrn = oddrn

    def to_data_entity(self) -> DataEntity:
        ...


class Postgres(Database):
    def to_data_entity(self) -> DataEntity:
        ...


class MySQL(Database):
    def to_data_entity(self) -> DataEntity:
        ...
