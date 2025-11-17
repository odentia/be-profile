from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Theme:
    """Тема пользователя"""
    user_id: str
    text_color: str = "#ffffff"
    main_bg_color: str = "#14141A"
    second_bg_color: str = "#272A33"
    contrast_color: str = "#6C63FF"
    highlight_color: str = "#A785FF"
    blur_transparency: int = 30  # 0-100
    updated_at: datetime = None

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()


@dataclass
class Profile:
    """Профиль пользователя"""
    user_id: str
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    email: str = ""
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

