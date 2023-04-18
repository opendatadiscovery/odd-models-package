from typing import Any, Iterable


def link_nodes(left, right) -> Any:
    if isinstance(left, Iterable):
        for asset in left:
            link_nodes(asset, right)
        return right

    if isinstance(right, Iterable):
        for asset in right:
            link_nodes(left, asset)

        return right

    if hasattr(left, "add_downstream"):
        left.add_downstream(right)

    if hasattr(right, "add_upstream"):
        right.add_upstream(left)

    return right
