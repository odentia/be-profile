from __future__ import annotations

from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from profile_service.domain.models import Profile, Theme
from profile_service.domain.repositories import ProfileRepository, ThemeRepository
from profile_service.domain.events import ProfileUpdatedEvent, ThemeUpdatedEvent, AccountDeletedEvent
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
    
    def __init__(self, profile_repo: ProfileRepository, event_publisher=None):
        self.profile_repo = profile_repo
        self.event_publisher = event_publisher
    
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
        
        # Публикуем событие обновления профиля
        if self.event_publisher:
            await self.event_publisher.publish(
                ProfileUpdatedEvent(
                    user_id=user_id,
                    name=updated_profile.name,
                    email=updated_profile.email,
                    description=updated_profile.description,
                    avatar_url=updated_profile.avatar_url
                )
            )
        
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
        deleted = await self.profile_repo.delete(user_id)
        
        # Публикуем событие удаления аккаунта
        if deleted and self.event_publisher:
            await self.event_publisher.publish(
                AccountDeletedEvent(user_id=user_id)
            )
        
        return deleted


class ThemeService:
    """Сервис для работы с темами"""
    
    def __init__(self, theme_repo: ThemeRepository, event_publisher=None):
        self.theme_repo = theme_repo
        self.event_publisher = event_publisher
    
    async def get_theme(self, user_id: str) -> ThemeResponse:
        """Получить тему пользователя"""
        theme = await self.theme_repo.get_by_user_id(user_id)
        if not theme:
            # Возвращаем тему по умолчанию
            default_theme = Theme(user_id=user_id)
            return ThemeResponse(
                user_id=default_theme.user_id,
                backgroundColor=default_theme.backgroundColor,
                backgroundColorMain=default_theme.backgroundColorMain,
                backgroundColorSub=default_theme.backgroundColorSub,
                boxShadow=default_theme.boxShadow,
                danger=default_theme.danger,
                border=default_theme.border,
                subtext=default_theme.subtext,
                text=default_theme.text,
                attention=default_theme.attention,
                glowColor=default_theme.glowColor,
                glowOpacity=default_theme.glowOpacity,
                cards=default_theme.cards,
                circleColor=default_theme.circleColor,
                updated_at=default_theme.updated_at
            )
        
        return ThemeResponse(
            user_id=theme.user_id,
            backgroundColor=theme.backgroundColor,
            backgroundColorMain=theme.backgroundColorMain,
            backgroundColorSub=theme.backgroundColorSub,
            boxShadow=theme.boxShadow,
            danger=theme.danger,
            border=theme.border,
            subtext=theme.subtext,
            text=theme.text,
            attention=theme.attention,
            glowColor=theme.glowColor,
            glowOpacity=theme.glowOpacity,
            cards=theme.cards,
            circleColor=theme.circleColor,
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
        if request.backgroundColor is not None:
            theme.backgroundColor = request.backgroundColor
        if request.backgroundColorMain is not None:
            theme.backgroundColorMain = request.backgroundColorMain
        if request.backgroundColorSub is not None:
            theme.backgroundColorSub = request.backgroundColorSub
        if request.boxShadow is not None:
            theme.boxShadow = request.boxShadow
        if request.danger is not None:
            theme.danger = request.danger
        if request.border is not None:
            theme.border = request.border
        if request.subtext is not None:
            theme.subtext = request.subtext
        if request.text is not None:
            theme.text = request.text
        if request.attention is not None:
            theme.attention = request.attention
        if request.glowColor is not None:
            theme.glowColor = request.glowColor
        if request.glowOpacity is not None:
            theme.glowOpacity = request.glowOpacity
        if request.cards is not None:
            theme.cards = request.cards
        if request.circleColor is not None:
            theme.circleColor = request.circleColor
        
        theme.updated_at = datetime.utcnow()
        
        existing_theme = await self.theme_repo.get_by_user_id(user_id)
        if existing_theme:
            updated_theme = await self.theme_repo.update(theme)
        else:
            updated_theme = await self.theme_repo.create(theme)
        
        # Публикуем событие обновления темы
        if self.event_publisher:
            await self.event_publisher.publish(
                ThemeUpdatedEvent(user_id=user_id)
            )
        
        return ThemeResponse(
            user_id=updated_theme.user_id,
            backgroundColor=updated_theme.backgroundColor,
            backgroundColorMain=updated_theme.backgroundColorMain,
            backgroundColorSub=updated_theme.backgroundColorSub,
            boxShadow=updated_theme.boxShadow,
            danger=updated_theme.danger,
            border=updated_theme.border,
            subtext=updated_theme.subtext,
            text=updated_theme.text,
            attention=updated_theme.attention,
            glowColor=updated_theme.glowColor,
            glowOpacity=updated_theme.glowOpacity,
            cards=updated_theme.cards,
            circleColor=updated_theme.circleColor,
            updated_at=updated_theme.updated_at
        )
    
    async def get_theme_by_user_id(self, user_id: str) -> Optional[ThemeResponse]:
        """Получить тему пользователя по его ID (публичный метод)"""
        theme = await self.theme_repo.get_by_user_id(user_id)
        if not theme:
            return None
        
        return ThemeResponse(
            user_id=theme.user_id,
            backgroundColor=theme.backgroundColor,
            backgroundColorMain=theme.backgroundColorMain,
            backgroundColorSub=theme.backgroundColorSub,
            boxShadow=theme.boxShadow,
            danger=theme.danger,
            border=theme.border,
            subtext=theme.subtext,
            text=theme.text,
            attention=theme.attention,
            glowColor=theme.glowColor,
            glowOpacity=theme.glowOpacity,
            cards=theme.cards,
            circleColor=theme.circleColor,
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
            backgroundColor=source_theme.backgroundColor,
            backgroundColorMain=source_theme.backgroundColorMain,
            backgroundColorSub=source_theme.backgroundColorSub,
            boxShadow=source_theme.boxShadow,
            danger=source_theme.danger,
            border=source_theme.border,
            subtext=source_theme.subtext,
            text=source_theme.text,
            attention=source_theme.attention,
            glowColor=source_theme.glowColor,
            glowOpacity=source_theme.glowOpacity,
            cards=source_theme.cards,
            circleColor=source_theme.circleColor
        )
        
        # Обновляем тему целевого пользователя
        return await self.update_theme(target_user_id, import_request)