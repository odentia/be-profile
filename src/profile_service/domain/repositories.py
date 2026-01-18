from __future__ import annotations

from typing import Optional, Protocol
from profile_service.domain.models import Profile, Theme


class ProfileRepository(Protocol):
    """Репозиторий для работы с профилями"""

    async def get_by_user_id(self, user_id: str) -> Optional[Profile]:
        """Получить профиль по ID пользователя"""
        ...

    async def create(self, profile: Profile) -> Profile:
        """Создать новый профиль"""
        ...

    async def update(self, profile: Profile) -> Profile:
        """Обновить профиль"""
        ...

    async def delete(self, user_id: str) -> bool:
        """Удалить профиль"""
        ...


class ThemeRepository(Protocol):
    """Репозиторий для работы с темами"""

    async def get_by_user_id(self, user_id: str) -> Optional[Theme]:
        """Получить тему по ID пользователя"""
        ...

    async def create(self, theme: Theme) -> Theme:
        """Создать новую тему"""
        ...

    async def update(self, theme: Theme) -> Theme:
        """Обновить тему"""
        ...
