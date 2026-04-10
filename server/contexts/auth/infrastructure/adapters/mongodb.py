from pymongo import ASCENDING, MongoClient

from contexts.auth.domain import AuthAccountRecord


class MongoAuthAccountRepository:
    def __init__(self, mongodb_url: str, database_name: str) -> None:
        self.client = MongoClient(mongodb_url)
        self.collection = self.client[database_name]["auth_accounts"]

    def initialize(self) -> None:
        self.collection.create_index([("email", ASCENDING)], unique=True)

    def seed_accounts(self, accounts: list[AuthAccountRecord]) -> None:
        for account in accounts:
            self.collection.update_one({"id": account.id}, {"$set": account.model_dump()}, upsert=True)

    def get_by_email(self, email: str) -> AuthAccountRecord | None:
        record = self.collection.find_one({"email": email}, {"_id": 0})
        return AuthAccountRecord(**record) if record else None

    def get_by_id(self, user_id: str) -> AuthAccountRecord | None:
        record = self.collection.find_one({"id": user_id}, {"_id": 0})
        return AuthAccountRecord(**record) if record else None
