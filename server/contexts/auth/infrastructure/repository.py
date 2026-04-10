from functools import lru_cache
from typing import TYPE_CHECKING

from config import get_settings
from contexts.auth.infrastructure.adapters.memory import MemoryAuthAccountRepository
from contexts.auth.infrastructure.adapters.mongodb import MongoAuthAccountRepository
from contexts.auth.infrastructure.adapters.sqlalchemy import (
    MariaDbAuthAccountRepository,
    MySqlAuthAccountRepository,
    PostgresAuthAccountRepository,
)

if TYPE_CHECKING:
    from contexts.auth.application.ports import AuthAccountRepository


@lru_cache
def get_auth_repository() -> "AuthAccountRepository":
    settings = get_settings()
    if settings.database_backend == "postgres":
        return PostgresAuthAccountRepository(settings.postgres_url)
    if settings.database_backend == "mysql":
        return MySqlAuthAccountRepository(settings.mysql_url)
    if settings.database_backend == "mariadb":
        return MariaDbAuthAccountRepository(settings.mariadb_url)
    if settings.database_backend == "mongodb":
        return MongoAuthAccountRepository(settings.mongodb_url, settings.mongodb_database)
    return MemoryAuthAccountRepository()
