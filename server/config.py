from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Template Server"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    database_backend: Literal["memory", "postgres", "mysql", "mariadb", "mongodb"] = "memory"
    postgres_url: str = "postgresql+psycopg://template:template@postgres:5432/template"
    mysql_url: str = "mysql+pymysql://template:template@mysql:3306/template"
    mariadb_url: str = "mysql+pymysql://template:template@mariadb:3306/template"
    mongodb_url: str = "mongodb://mongo:27017"
    mongodb_database: str = "template"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_ttl_minutes: int = 120
    bootstrap_admin_email: str = "admin@example.com"
    bootstrap_admin_password: str = "<CHANGE_ME>"
    bootstrap_admin_name: str = "Template Admin"
    bootstrap_operator_email: str = "operator@example.com"
    bootstrap_operator_password: str = "<CHANGE_ME>"
    bootstrap_operator_name: str = "Template Operator"
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3001",
            "http://localhost:3002",
            "http://127.0.0.1:3002",
            "http://localhost:4000",
            "http://127.0.0.1:4000",
        ]
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
