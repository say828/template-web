from functools import lru_cache

from fastapi import HTTPException, status

from config import get_settings
from contexts.auth.domain import AuthAccountRecord, AuthenticatedUser, AuthToken, LoginCommand
from contexts.auth.infrastructure import (
    decode_access_token,
    get_auth_repository,
    issue_access_token,
    verify_password,
)
from data.bootstrap_loader import load_bootstrap_json
from shared.infrastructure import hash_password


def authenticate_user(command: LoginCommand) -> AuthToken:
    prepare_auth_store()
    repository = get_auth_repository()
    account = repository.get_by_email(str(command.email))
    if account is None or not verify_password(command.password, account.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return AuthToken(access_token=issue_access_token(account.id), user_id=account.id)


def resolve_current_user(bearer_token: str) -> AuthenticatedUser:
    prepare_auth_store()
    subject = decode_access_token(bearer_token)
    if subject is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    repository = get_auth_repository()
    account = repository.get_by_id(subject)
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return AuthenticatedUser(**account.model_dump(exclude={"password_hash"}))


def prepare_auth_store() -> None:
    _seed_auth_store()


@lru_cache
def _seed_auth_store() -> None:
    settings = get_settings()
    repository = get_auth_repository()
    repository.initialize()
    password_lookup = {
        "bootstrap_admin_password": settings.bootstrap_admin_password,
        "bootstrap_operator_password": settings.bootstrap_operator_password,
    }
    accounts = [
        AuthAccountRecord(
            id=entry["id"],
            name=entry["name"],
            email=entry["email"],
            role=entry["role"],
            status=entry["status"],
            password_hash=hash_password(password_lookup[entry["password_source"]]),
        )
        for entry in load_bootstrap_json("auth_accounts.json")
    ]
    repository.seed_accounts(accounts)
