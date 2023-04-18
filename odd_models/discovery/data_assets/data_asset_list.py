from collections import UserList

from ..helper import link_nodes
from .data_asset import HasUpstream


class DataAssetsList(UserList):
    """A list of DataAssets that can be connected to another DataAsset."""

    def __init__(self, data_assets: list):
        super().__init__(initlist=data_assets)

    def __rshift__(self, other: HasUpstream) -> HasUpstream:
        return link_nodes(self, other)

    def __repr__(self):
        return f"{[x for x in self]}"
