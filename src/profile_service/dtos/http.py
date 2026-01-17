from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl

# TODO: В будущем импортировать из contracts.http.profile
# from contracts.http.profile import (
#     ProfileUpdateRequest,
#     ProfileResponse,
#     ThemeUpdateRequest,
#     ThemeResponse,
#     PasswordChangeRequest,
#     DeleteAccountRequest
# )


class ThemeUpdateRequest(BaseModel):
    """Запрос на обновление темы"""
    backgroundColor: Optional[str] = None
    backgroundColorMain: Optional[str] = None
    backgroundColorSub: Optional[str] = None
    boxShadow: Optional[str] = None
    danger: Optional[str] = None
    border: Optional[str] = None
    subtext: Optional[str] = None
    text: Optional[str] = None
    attention: Optional[str] = None
    glowColor: Optional[str] = None
    glowOpacity: Optional[str] = None
    cards: Optional[str] = None
    circleColor: Optional[str] = None


class ThemeResponse(BaseModel):
    """Ответ с темой"""
    user_id: str
    backgroundColor: str
    backgroundColorMain: str
    backgroundColorSub: str
    boxShadow: str
    danger: str
    border: str
    subtext: str
    text: str
    attention: str
    glowColor: str
    glowOpacity: str
    cards: str
    circleColor: str
    updated_at: datetime


class ProfileUpdateRequest(BaseModel):
    """Запрос на обновление профиля"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[HttpUrl] = None
    email: Optional[EmailStr] = None


class ProfileResponse(BaseModel):
    """Ответ с профилем"""
    user_id: str
    name: str
    description: Optional[str]
    avatar_url: Optional[str]
    email: str
    created_at: datetime
    updated_at: datetime


class PasswordChangeRequest(BaseModel):
    """Запрос на изменение пароля"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class DeleteAccountRequest(BaseModel):
    """Запрос на удаление аккаунта"""
    password: str  # Подтверждение паролем


class ThemeImportRequest(BaseModel):
    """Запрос на импорт темы от другого пользователя"""
    user_id: str = Field(..., description="ID пользователя, чью тему нужно импортировать")
