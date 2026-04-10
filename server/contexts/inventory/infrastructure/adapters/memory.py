from contexts.inventory.domain import InventoryLevelRecord


class MemoryInventoryRepository:
    def __init__(self) -> None:
        self._levels: dict[tuple[str, str], InventoryLevelRecord] = {}

    def initialize(self) -> None:
        return None

    def seed_levels(self, levels: list[InventoryLevelRecord]) -> None:
        for level in levels:
            self._levels[(level.sku, level.location_id)] = level.model_copy(deep=True)

    def list_levels(self) -> list[InventoryLevelRecord]:
        return [level.model_copy(deep=True) for level in self._levels.values()]

    def get_level(self, sku: str, location_id: str) -> InventoryLevelRecord | None:
        level = self._levels.get((sku, location_id))
        return level.model_copy(deep=True) if level is not None else None

    def upsert_level(self, level: InventoryLevelRecord) -> InventoryLevelRecord:
        self._levels[(level.sku, level.location_id)] = level.model_copy(deep=True)
        return level.model_copy(deep=True)
