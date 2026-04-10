from functools import lru_cache

from contexts.inventory.infrastructure.adapters.memory import MemoryInventoryRepository


@lru_cache
def get_inventory_repository() -> MemoryInventoryRepository:
    return MemoryInventoryRepository()
