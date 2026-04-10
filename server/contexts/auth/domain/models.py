from pydantic import BaseModel, EmailStr


class LoginCommand(BaseModel):
    email: EmailStr
    password: str


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str


class AuthenticatedUser(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    status: str


class AuthAccountRecord(AuthenticatedUser):
    password_hash: str
