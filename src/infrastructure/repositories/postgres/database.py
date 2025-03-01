from contextvars import ContextVar
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .models.base import BaseORM


class Database:

    def __init__(self, uri: str):
        self._engine = create_async_engine(
            uri,
            pool_pre_ping=True,
            pool_size=20,
            echo_pool="debug",
            echo=True,
        )
        self._session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=True,
            bind=self._engine,
        )
        self._session_context: AsyncSession | None = ContextVar(
            "session_context",
            default=None,
        )

    def start_session(self) -> AsyncSession:
        if not self._session_context.get():
            self._session_context.set(self._session())
        return self._session_context.get()

    def get_session(self) -> AsyncSession | None:
        return self._session_context.get()
    
    async def create_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(BaseORM.metadata.create_all)