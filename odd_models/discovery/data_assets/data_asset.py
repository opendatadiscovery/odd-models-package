from typing import Protocol, runtime_checkable

from odd_models.models import DataEntity


class DataAsset(Protocol):
    """A DataAsset is a logical representation of a data entity"""

    oddrn: str


class MappableToDataEntity(DataAsset, Protocol):
    """A DataAsset that can be mapped to a DataEntity"""

    def to_data_entity(self) -> DataEntity:
        ...


@runtime_checkable
class HasUpstream(DataAsset, Protocol):
    """A DataAsset that has upstream DataAssets"""

    upstream: list[str]

    def add_upstream(self, data_asset: DataAsset) -> None:
        self.upstream.append(data_asset.oddrn)


@runtime_checkable
class HasDownstream(DataAsset, Protocol):
    """A DataAsset that has downstream DataAssets"""

    downstream: list[str]

    def add_downstream(self, data_asset: DataAsset):
        self.downstream.append(data_asset.oddrn)


class Transformer(HasUpstream, HasDownstream, Protocol):
    """A DataAsset that transforms other DataAssets"""

    ...


class Upstream(Protocol):
    """A DataAsset that is upstream of other DataAssets"""

    def __rshift__(self, other: HasUpstream) -> HasUpstream:
        ...
