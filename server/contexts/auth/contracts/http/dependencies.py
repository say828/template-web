from fastapi import Depends, Header, HTTPException, status

from contexts.auth.application import resolve_current_user
from contexts.auth.domain import AuthenticatedUser


def _extract_bearer_token(authorization: str | None) -> str:
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.casefold() != "bearer" or not token.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )
    return token.strip()


def require_authenticated_user(
    authorization: str | None = Header(default=None),
) -> AuthenticatedUser:
    return resolve_current_user(_extract_bearer_token(authorization))


def require_admin_user(
    current_user: AuthenticatedUser = Depends(require_authenticated_user),
) -> AuthenticatedUser:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user
