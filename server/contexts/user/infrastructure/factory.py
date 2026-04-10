from functools import lru_cache
from typing import TYPE_CHECKING

from config import get_settings
from contexts.user.infrastructure.adapters.memory import MemoryUserRepository
from contexts.user.infrastructure.adapters.mongodb import MongoUserRepository
from contexts.user.infrastructure.adapters.sqlalchemy import (
    MariaDbUserRepository,
    MySqlUserRepository,
    PostgresUserRepository,
)

if TYPE_CHECKING:
    from contexts.user.application.ports import UserRepository


@lru_cache
def get_user_repository() -> "UserRepository":
    settings = get_settings()
    if settings.database_backend == "postgres":
        return PostgresUserRepository(settings.postgres_url)
    if settings.database_backend == "mysql":
        return MySqlUserRepository(settings.mysql_url)
    if settings.database_backend == "mariadb":
        return MariaDbUserRepository(settings.mariadb_url)
    if settings.database_backend == "mongodb":
        return MongoUserRepository(settings.mongodb_url, settings.mongodb_database)
    return MemoryUserRepository()
