from sqlalchemy import String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from contexts.auth.domain import AuthAccountRecord


class Base(DeclarativeBase):
    pass


class AuthAccountTable(Base):
    __tablename__ = "auth_accounts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))
    password_hash: Mapped[str] = mapped_column(String(255))


class SqlAlchemyAuthAccountRepository:
    def __init__(self, database_url: str) -> None:
        self.engine = create_engine(database_url, future=True)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    def initialize(self) -> None:
        Base.metadata.create_all(self.engine)

    def seed_accounts(self, accounts: list[AuthAccountRecord]) -> None:
        with self.session_factory() as session:
            for account in accounts:
                existing = session.get(AuthAccountTable, account.id)
                if existing is None:
                    session.add(AuthAccountTable(**account.model_dump()))
                    continue
                for field, value in account.model_dump().items():
                    setattr(existing, field, value)
            session.commit()

    def get_by_email(self, email: str) -> AuthAccountRecord | None:
        with self.session_factory() as session:
            record = session.scalar(select(AuthAccountTable).where(AuthAccountTable.email == email))
            return self._to_record(record)

    def get_by_id(self, user_id: str) -> AuthAccountRecord | None:
        with self.session_factory() as session:
            record = session.get(AuthAccountTable, user_id)
            return self._to_record(record)

    @staticmethod
    def _to_record(record: AuthAccountTable | None) -> AuthAccountRecord | None:
        if record is None:
            return None
        return AuthAccountRecord(
            id=record.id,
            name=record.name,
            email=record.email,
            role=record.role,
            status=record.status,
            password_hash=record.password_hash,
        )


class PostgresAuthAccountRepository(SqlAlchemyAuthAccountRepository):
    pass


class MySqlAuthAccountRepository(SqlAlchemyAuthAccountRepository):
    pass


class MariaDbAuthAccountRepository(SqlAlchemyAuthAccountRepository):
    pass
