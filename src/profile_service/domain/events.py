from __future__ import annotations

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProfileEvent(BaseModel):
    """Базовое событие профиля"""

    event_type: str
    timestamp: datetime = datetime.utcnow()
    service: str = "profile-service"


class ProfileUpdatedEvent(ProfileEvent):
    """Событие обновления профиля"""

    event_type: str = "profile_updated"
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None


class ThemeUpdatedEvent(ProfileEvent):
    """Событие обновления темы"""

    event_type: str = "theme_updated"
    user_id: str


class AccountDeletedEvent(ProfileEvent):
    """Событие удаления аккаунта"""

    event_type: str = "account_deleted"
    user_id: str
