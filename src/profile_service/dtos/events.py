from __future__ import annotations

# TODO: Импортировать из contracts.events.profile_v1
# from contracts.events.profile_v1 import (
#     ProfileUpdatedV1,
#     ThemeUpdatedV1,
#     AccountDeletedV1
# )

# Временные схемы событий (будут заменены на contracts)
from pydantic import BaseModel
from datetime import datetime


class ProfileUpdatedV1(BaseModel):
    """Событие обновления профиля"""

    user_id: str
    name: str
    email: str
    updated_at: datetime


class ThemeUpdatedV1(BaseModel):
    """Событие обновления темы"""

    user_id: str
    updated_at: datetime


class AccountDeletedV1(BaseModel):
    """Событие удаления аккаунта"""

    user_id: str
    deleted_at: datetime
