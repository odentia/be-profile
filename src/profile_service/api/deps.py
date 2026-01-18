from __future__ import annotations

from typing import AsyncIterator, Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from profile_service.core.config import Settings
from profile_service.core.logging import get_logger
from profile_service.domain.services import PasswordService
from profile_service.repo.sql.repositories import SQLProfileRepository, SQLThemeRepository
from profile_service.mq.publisher import EventPublisher

log = get_logger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


def get_settings(request: Request) -> Settings:
    """Получить настройки из app state"""
    settings: Settings = request.app.state.settings
    return settings


def _get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    sf: async_sessionmaker[AsyncSession] | None = getattr(
        request.app.state, "session_factory", None
    )
    if sf is None:
        from profile_service.core.db import get_session_factory as _fallback_get_sf

        sf = _fallback_get_sf()
    if sf is None:
        raise RuntimeError("Session factory is not initialized. Check lifespan startup.")
    return sf


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    session_factory = _get_session_factory(request)
    async with session_factory() as session:
        yield session


def get_password_service() -> PasswordService:
    """Получить сервис для работы с паролями"""
    return PasswordService()


def get_profile_repo(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SQLProfileRepository:
    """Получить репозиторий профилей"""
    return SQLProfileRepository(session)


def get_theme_repo(session: Annotated[AsyncSession, Depends(get_session)]) -> SQLThemeRepository:
    """Получить репозиторий тем"""
    return SQLThemeRepository(session)


def get_event_publisher(request: Request) -> EventPublisher | None:
    """Получить event publisher из app state"""
    return getattr(request.app.state, "event_publisher", None)


async def get_current_token(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> str:
    return "" if creds is None else creds.credentials


async def get_current_user_id(request: Request) -> str:
    """Получить ID текущего пользователя из JWT токена"""
    # Извлекаем токен из заголовка Authorization
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]

    # TODO: Интеграция с auth-service для проверки токена
    # Пока проверяем локально через JWT
    from jose import jwt

    settings = request.app.state.settings
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
