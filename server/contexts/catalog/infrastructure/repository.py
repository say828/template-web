from functools import lru_cache

from contexts.catalog.infrastructure.adapters.memory import MemoryCatalogRepository


@lru_cache
def get_catalog_repository() -> MemoryCatalogRepository:
    return MemoryCatalogRepository()
