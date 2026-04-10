from fastapi import HTTPException, status

from contexts.user.domain import UpdateUserStatusCommand, UserDetail, UserRecord, UserSummary
from contexts.user.infrastructure import get_user_repository
from data.bootstrap_loader import load_bootstrap_json


def list_user_summaries() -> list[UserSummary]:
    repository = get_user_repository()
    return repository.list_summaries()


def get_user_or_404(user_id: str) -> UserDetail:
    repository = get_user_repository()
    user = repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserDetail(**user.model_dump())


def update_user_status_or_404(user_id: str, command: UpdateUserStatusCommand) -> UserDetail:
    repository = get_user_repository()
    user = repository.update_status(user_id, command.status)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserDetail(**user.model_dump())


def prepare_user_store() -> None:
    repository = get_user_repository()
    repository.initialize()
    records = [
        UserRecord(
            id=entry["id"],
            name=entry["name"],
            email=entry["email"],
            role=entry["role"],
            status=entry["status"],
            timezone=entry["timezone"],
            last_login_at=entry["last_login_at"],
        )
        for entry in load_bootstrap_json("users.json")
    ]
    repository.seed_users(records)
