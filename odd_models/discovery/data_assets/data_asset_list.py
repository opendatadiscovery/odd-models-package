from collections import UserList

from odd_models.discovery.data_assets.data_asset import HasUpstream
from odd_models.discovery.helper import link_nodes


class DataAssetsList(UserList):
    """A list of DataAssets that can be connected to another DataAsset."""

    def __init__(self, data_assets: list):
        super().__init__(initlist=data_assets)

    def __rshift__(self, other: HasUpstream) -> HasUpstream:
        return link_nodes(self, other)

    def __repr__(self):
        return f"{[x for x in self]}"
