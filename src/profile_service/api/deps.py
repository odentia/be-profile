from __future__ import annotations

from typing import AsyncIterator, Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from profile_service.core.config import Settings
from profile_service.core.logging import get_logger
from profile_service.domain.services import PasswordService, JWTService
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


def get_jwt_service(settings: SettingsDep) -> JWTService:
    """Получить сервис для работы с JWT"""
    return JWTService(settings)


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
    request: Request,
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)] = None,
) -> str:
    """Получить токен из кук или заголовка Authorization (приоритет у кук)
    
    Работает в двух режимах:
    1. С куками (для браузеров) - проверяет куку access_token
    2. С заголовками (для API клиентов) - проверяет Authorization: Bearer <token>
    """
    # 1. Проверяем куки (приоритет для HTTP-only, используется браузерами)
    access_token_cookie = request.cookies.get("access_token")
    if access_token_cookie:
        return access_token_cookie
    
    # 2. Если нет в куках, проверяем заголовок Authorization (для API клиентов)
    if creds and creds.credentials:
        return creds.credentials
    
    # Также проверяем заголовок напрямую (на случай, если HTTPBearer не сработал)
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    
    return ""


async def get_current_user_id(
    request: Request,
    token: Annotated[str, Depends(get_current_token)],
    settings: SettingsDep,
) -> str:
    """Получить ID текущего пользователя из JWT токена"""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Проверяем JWT токен через JWTService
    jwt_service = JWTService(settings)
    payload = jwt_service.verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


SettingsDep = Annotated[Settings, Depends(get_settings)]
SessionDep = Annotated[AsyncSession, Depends(get_session)]
