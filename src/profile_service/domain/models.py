from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Theme:
    """Тема пользователя"""
    user_id: str
    backgroundColor: str = "#14141A"
    backgroundColorMain: str = "#14141A"
    backgroundColorSub: str = "#272A33"
    boxShadow: str = "rgba(0, 0, 0, 0.1)"
    danger: str = "#ff4444"
    border: str = "#272A33"
    subtext: str = "#a0a0a0"
    text: str = "#ffffff"
    attention: str = "#ffaa00"
    glowColor: str = "#6C63FF"
    glowOpacity: str = "0.3"
    cards: str = "#1e1e24"
    circleColor: str = "#6C63FF"
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

