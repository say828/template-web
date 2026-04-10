from fastapi import APIRouter, Depends

from contexts.auth.application import authenticate_user
from contexts.auth.contracts.http.dependencies import require_authenticated_user
from contexts.auth.domain import AuthToken, AuthenticatedUser, LoginCommand

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthToken)
def login(command: LoginCommand) -> AuthToken:
    return authenticate_user(command)


@router.get("/me", response_model=AuthenticatedUser)
def me(
    current_user: AuthenticatedUser = Depends(require_authenticated_user),
) -> AuthenticatedUser:
    return current_user
