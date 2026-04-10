from .services import (
    adjust_inventory_level_or_404,
    get_inventory_level_or_404,
    list_inventory_levels,
    prepare_inventory_store,
    release_inventory_level_or_404,
    reserve_inventory_or_404,
    set_inventory_level_or_404,
)

adjust_inventory_level = adjust_inventory_level_or_404
release_inventory_level = release_inventory_level_or_404
reserve_inventory_level = reserve_inventory_or_404
set_inventory_level = set_inventory_level_or_404

__all__ = [
    "adjust_inventory_level",
    "adjust_inventory_level_or_404",
    "get_inventory_level_or_404",
    "list_inventory_levels",
    "prepare_inventory_store",
    "release_inventory_level",
    "release_inventory_level_or_404",
    "reserve_inventory_level",
    "reserve_inventory_or_404",
    "set_inventory_level",
    "set_inventory_level_or_404",
]
