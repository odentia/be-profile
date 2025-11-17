from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from profile_service.core.logging import get_logger

log = get_logger(__name__)

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


async def init_engine(url: str, echo: bool = False) -> AsyncEngine:
    global _engine
    if _engine is None:
        _engine = create_async_engine(url, echo=echo, pool_pre_ping=True)
        log.info("Database engine initialized", extra={"url": url.split("@")[-1] if "@" in url else url})
    return _engine


def init_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(engine, expire_on_commit=False)
        log.info("Session factory initialized")
    return _session_factory


async def close_engine() -> None:
    global _engine, _session_factory
    if _engine:
        await _engine.dispose()
        _engine = None
        _session_factory = None
        log.info("Database engine closed")


def get_session_factory() -> async_sessionmaker[AsyncSession] | None:
    return _session_factory

