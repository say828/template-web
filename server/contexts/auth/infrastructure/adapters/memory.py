from contexts.auth.domain import AuthAccountRecord


class MemoryAuthAccountRepository:
    def __init__(self) -> None:
        self._accounts: dict[str, AuthAccountRecord] = {}

    def initialize(self) -> None:
        return None

    def seed_accounts(self, accounts: list[AuthAccountRecord]) -> None:
        for account in accounts:
            self._accounts[account.id] = account

    def get_by_email(self, email: str) -> AuthAccountRecord | None:
        return next((account for account in self._accounts.values() if account.email == email), None)

    def get_by_id(self, user_id: str) -> AuthAccountRecord | None:
        return self._accounts.get(user_id)
