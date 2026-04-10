from pydantic import BaseModel, EmailStr


class UserSummary(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    status: str


class UserDetail(UserSummary):
    timezone: str
    last_login_at: str


class UserRecord(UserDetail):
    pass


class UpdateUserStatusCommand(BaseModel):
    status: str
