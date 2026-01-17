from __future__ import annotations

from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from profile_service.domain.models import Profile, Theme
from profile_service.domain.repositories import ProfileRepository, ThemeRepository
from profile_service.dtos.http import (
    ProfileUpdateRequest, ProfileResponse,
    ThemeUpdateRequest, ThemeResponse,
    ThemeImportRequest,
    PasswordChangeRequest
)


class PasswordService:
    """Сервис для работы с паролями"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверка пароля"""
        return self.pwd_context.verify(plain_password, hashed_password)


class ProfileService:
    """Сервис для работы с профилями"""
    
    def __init__(self, profile_repo: ProfileRepository):
        self.profile_repo = profile_repo
    
    async def get_profile(self, user_id: str) -> Optional[ProfileResponse]:
        """Получить профиль пользователя"""
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            return None
        
        return ProfileResponse(
            user_id=profile.user_id,
            name=profile.name,
            description=profile.description,
            avatar_url=profile.avatar_url,
            email=profile.email,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
    
    async def update_profile(
        self, 
        user_id: str, 
        request: ProfileUpdateRequest
    ) -> Optional[ProfileResponse]:
        """Обновить профиль пользователя"""
        profile = await self.profile_repo.get_by_user_id(user_id)
        if not profile:
            return None
        
        # Обновляем только переданные поля
        if request.name is not None:
            profile.name = request.name
        if request.description is not None:
            profile.description = request.description
        if request.avatar_url is not None:
            profile.avatar_url = str(request.avatar_url)
        if request.email is not None:
            profile.email = request.email
        
        profile.updated_at = datetime.utcnow()
        
        updated_profile = await self.profile_repo.update(profile)
        
        return ProfileResponse(
            user_id=updated_profile.user_id,
            name=updated_profile.name,
            description=updated_profile.description,
            avatar_url=updated_profile.avatar_url,
            email=updated_profile.email,
            created_at=updated_profile.created_at,
            updated_at=updated_profile.updated_at
        )
    
    async def delete_profile(self, user_id: str) -> bool:
        """Удалить профиль"""
        return await self.profile_repo.delete(user_id)


class ThemeService:
    """Сервис для работы с темами"""
    
    def __init__(self, theme_repo: ThemeRepository):
        self.theme_repo = theme_repo
    
    async def get_theme(self, user_id: str) -> ThemeResponse:
        """Получить тему пользователя"""
        theme = await self.theme_repo.get_by_user_id(user_id)
        if not theme:
            # Возвращаем тему по умолчанию
            default_theme = Theme(user_id=user_id)
            return ThemeResponse(
                user_id=default_theme.user_id,
                text_color=default_theme.text_color,
                main_bg_color=default_theme.main_bg_color,
                second_bg_color=default_theme.second_bg_color,
                contrast_color=default_theme.contrast_color,
                highlight_color=default_theme.highlight_color,
                blur_transparency=default_theme.blur_transparency,
                updated_at=default_theme.updated_at
            )
        
        return ThemeResponse(
            user_id=theme.user_id,
            text_color=theme.text_color,
            main_bg_color=theme.main_bg_color,
            second_bg_color=theme.second_bg_color,
            contrast_color=theme.contrast_color,
            highlight_color=theme.highlight_color,
            blur_transparency=theme.blur_transparency,
            updated_at=theme.updated_at
        )
    
    async def update_theme(
        self, 
        user_id: str, 
        request: ThemeUpdateRequest
    ) -> ThemeResponse:
        """Обновить тему пользователя"""
        theme = await self.theme_repo.get_by_user_id(user_id)
        
        if not theme:
            # Создаем новую тему
            theme = Theme(user_id=user_id)
        
        # Обновляем только переданные поля
        if request.text_color is not None:
            theme.text_color = request.text_color
        if request.main_bg_color is not None:
            theme.main_bg_color = request.main_bg_color
        if request.second_bg_color is not None:
            theme.second_bg_color = request.second_bg_color
        if request.contrast_color is not None:
            theme.contrast_color = request.contrast_color
        if request.highlight_color is not None:
            theme.highlight_color = request.highlight_color
        if request.blur_transparency is not None:
            theme.blur_transparency = request.blur_transparency
        
        theme.updated_at = datetime.utcnow()
        
        existing_theme = await self.theme_repo.get_by_user_id(user_id)
        if existing_theme:
            updated_theme = await self.theme_repo.update(theme)
        else:
            updated_theme = await self.theme_repo.create(theme)
        
        return ThemeResponse(
            user_id=updated_theme.user_id,
            text_color=updated_theme.text_color,
            main_bg_color=updated_theme.main_bg_color,
            second_bg_color=updated_theme.second_bg_color,
            contrast_color=updated_theme.contrast_color,
            highlight_color=updated_theme.highlight_color,
            blur_transparency=updated_theme.blur_transparency,
            updated_at=updated_theme.updated_at
        )
    
    async def get_theme_by_user_id(self, user_id: str) -> Optional[ThemeResponse]:
        """Получить тему пользователя по его ID (публичный метод)"""
        theme = await self.theme_repo.get_by_user_id(user_id)
        if not theme:
            return None
        
        return ThemeResponse(
            user_id=theme.user_id,
            text_color=theme.text_color,
            main_bg_color=theme.main_bg_color,
            second_bg_color=theme.second_bg_color,
            contrast_color=theme.contrast_color,
            highlight_color=theme.highlight_color,
            blur_transparency=theme.blur_transparency,
            updated_at=theme.updated_at
        )
    
    async def import_theme(
        self,
        target_user_id: str,
        source_user_id: str
    ) -> ThemeResponse:
        """Импортировать тему от другого пользователя в свой профиль"""
        # Получаем тему источника
        source_theme = await self.theme_repo.get_by_user_id(source_user_id)
        if not source_theme:
            return None
        
        # Создаем ThemeUpdateRequest из темы источника
        import_request = ThemeUpdateRequest(
            text_color=source_theme.text_color,
            main_bg_color=source_theme.main_bg_color,
            second_bg_color=source_theme.second_bg_color,
            contrast_color=source_theme.contrast_color,
            highlight_color=source_theme.highlight_color,
            blur_transparency=source_theme.blur_transparency
        )
        
        # Обновляем тему целевого пользователя
        return await self.update_theme(target_user_id, import_request)