from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from contexts.user.domain import UserRecord, UserSummary


class Base(DeclarativeBase):
    pass


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    timezone: Mapped[str] = mapped_column(String(64))
    last_login_at: Mapped[str] = mapped_column(String(64))


class SqlAlchemyUserRepository:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, future=True)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    def initialize(self) -> None:
        Base.metadata.create_all(self.engine)

    def seed_users(self, users: list[UserRecord]) -> None:
        with self.session_factory() as session:
            for user in users:
                existing = session.get(UserTable, user.id)
                if existing is None:
                    session.add(UserTable(**user.model_dump()))
                    continue
                for field, value in user.model_dump().items():
                    setattr(existing, field, value)
            session.commit()

    def get_by_id(self, user_id: str) -> UserRecord | None:
        with self.session_factory() as session:
            record = session.get(UserTable, user_id)
            return self._to_record(record)

    def list_summaries(self) -> list[UserSummary]:
        with self.session_factory() as session:
            records = session.scalars(select(UserTable).order_by(UserTable.id)).all()
            return [
                UserSummary(
                    id=record.id,
                    name=record.name,
                    email=record.email,
                    role=record.role,
                    status=record.status,
                )
                for record in records
            ]

    def update_status(self, user_id: str, status: str) -> UserRecord | None:
        with self.session_factory() as session:
            record = session.get(UserTable, user_id)
            if record is None:
                return None
            record.status = status
            session.commit()
            return self._to_record(record)

    @staticmethod
    def _to_record(record: UserTable | None) -> UserRecord | None:
        if record is None:
            return None
        return UserRecord(
            id=record.id,
            name=record.name,
            email=record.email,
            role=record.role,
            status=record.status,
            timezone=record.timezone,
            last_login_at=record.last_login_at,
        )


class PostgresUserRepository(SqlAlchemyUserRepository):
    pass


class MySqlUserRepository(SqlAlchemyUserRepository):
    pass


class MariaDbUserRepository(SqlAlchemyUserRepository):
    pass
