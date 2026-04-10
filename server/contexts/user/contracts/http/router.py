from fastapi import APIRouter, Depends

from contexts.auth.contracts.http.dependencies import require_admin_user
from contexts.user.application import get_user_or_404, list_user_summaries, update_user_status_or_404
from contexts.user.domain import UpdateUserStatusCommand, UserDetail, UserSummary

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(require_admin_user)],
)


@router.get("", response_model=list[UserSummary])
def list_users() -> list[UserSummary]:
    return list_user_summaries()


@router.get("/{user_id}", response_model=UserDetail)
def get_user(user_id: str) -> UserDetail:
    return get_user_or_404(user_id)


@router.patch("/{user_id}/status", response_model=UserDetail)
def update_user_status(user_id: str, command: UpdateUserStatusCommand) -> UserDetail:
    return update_user_status_or_404(user_id, command)
