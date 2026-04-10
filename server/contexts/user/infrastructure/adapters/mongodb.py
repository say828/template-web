from pymongo import ASCENDING, MongoClient, ReturnDocument

from contexts.user.domain import UserRecord, UserSummary


class MongoUserRepository:
    def __init__(self, mongodb_url: str, database_name: str) -> None:
        self.client = MongoClient(mongodb_url)
        self.collection = self.client[database_name]["users"]

    def initialize(self) -> None:
        self.collection.create_index([("email", ASCENDING)], unique=True)

    def seed_users(self, users: list[UserRecord]) -> None:
        for user in users:
            self.collection.update_one({"id": user.id}, {"$set": user.model_dump()}, upsert=True)

    def get_by_id(self, user_id: str) -> UserRecord | None:
        record = self.collection.find_one({"id": user_id}, {"_id": 0})
        return UserRecord(**record) if record else None

    def list_summaries(self) -> list[UserSummary]:
        return [
            UserSummary(
                id=record["id"],
                name=record["name"],
                email=record["email"],
                role=record["role"],
                status=record["status"],
            )
            for record in self.collection.find({}, {"_id": 0}).sort("id", ASCENDING)
        ]

    def update_status(self, user_id: str, status: str) -> UserRecord | None:
        record = self.collection.find_one_and_update(
            {"id": user_id},
            {"$set": {"status": status}},
            return_document=ReturnDocument.AFTER,
            projection={"_id": 0},
        )
        return UserRecord(**record) if record else None
