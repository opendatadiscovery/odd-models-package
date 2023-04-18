from odd_models.models import DataEntity

from .data_asset import DataAsset


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
