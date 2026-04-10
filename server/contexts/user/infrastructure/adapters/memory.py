from contexts.user.domain import UserRecord, UserSummary


class MemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, UserRecord] = {}

    def initialize(self) -> None:
        return None

    def seed_users(self, users: list[UserRecord]) -> None:
        for user in users:
            self._users[user.id] = user

    def get_by_id(self, user_id: str) -> UserRecord | None:
        return self._users.get(user_id)

    def list_summaries(self) -> list[UserSummary]:
        return [UserSummary(**user.model_dump(exclude={"timezone", "last_login_at"})) for user in self._users.values()]

    def update_status(self, user_id: str, status: str) -> UserRecord | None:
        user = self._users.get(user_id)
        if user is None:
            return None
        updated_user = user.model_copy(update={"status": status})
        self._users[user_id] = updated_user
        return updated_user
