from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.postgres.database import Database


class DBSessionNotStarted(Exception):
    pass


@dataclass
class BasePosgresRepository:
    database: Database

    @property
    def db_session(self) -> AsyncSession:
        session = self.database.get_session()
        if not session:
            raise DBSessionNotStarted()
        return session
