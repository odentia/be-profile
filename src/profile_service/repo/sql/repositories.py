from __future__ import annotations

from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from profile_service.domain.models import Profile, Theme
from profile_service.repo.sql.models import Profiles, Themes
from profile_service.repo.sql.mappers import (
    profile_to_domain,
    profile_to_model,
    theme_to_domain,
    theme_to_model,
)


class SQLProfileRepository:
    """SQLAlchemy реализация репозитория профилей"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: str) -> Optional[Profile]:
        """Получить профиль по ID пользователя"""
        result = await self.session.execute(select(Profiles).where(Profiles.user_id == user_id))
        profile_model = result.scalar_one_or_none()
        return profile_to_domain(profile_model) if profile_model else None

    async def create(self, profile: Profile) -> Profile:
        """Создать новый профиль"""
        profile_model = profile_to_model(profile)
        self.session.add(profile_model)
        await self.session.commit()
        await self.session.refresh(profile_model)
        return profile_to_domain(profile_model)

    async def update(self, profile: Profile) -> Profile:
        """Обновить профиль"""
        profile_model = profile_to_model(profile)
        await self.session.merge(profile_model)
        await self.session.commit()
        return profile

    async def delete(self, user_id: str) -> bool:
        """Удалить профиль"""
        result = await self.session.execute(delete(Profiles).where(Profiles.user_id == user_id))
        await self.session.commit()
        return result.rowcount > 0


class SQLThemeRepository:
    """SQLAlchemy реализация репозитория тем"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: str) -> Optional[Theme]:
        """Получить тему по ID пользователя"""
        result = await self.session.execute(select(Themes).where(Themes.user_id == user_id))
        theme_model = result.scalar_one_or_none()
        return theme_to_domain(theme_model) if theme_model else None

    async def create(self, theme: Theme) -> Theme:
        """Создать новую тему"""
        theme_model = theme_to_model(theme)
        self.session.add(theme_model)
        await self.session.commit()
        await self.session.refresh(theme_model)
        return theme_to_domain(theme_model)

    async def update(self, theme: Theme) -> Theme:
        """Обновить тему"""
        theme_model = theme_to_model(theme)
        await self.session.merge(theme_model)
        await self.session.commit()
        return theme
