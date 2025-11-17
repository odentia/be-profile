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
    text_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    main_bg_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    second_bg_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    contrast_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    highlight_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    blur_transparency: Optional[int] = Field(None, ge=0, le=100)


class ThemeResponse(BaseModel):
    """Ответ с темой"""
    user_id: str
    text_color: str
    main_bg_color: str
    second_bg_color: str
    contrast_color: str
    highlight_color: str
    blur_transparency: int
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

