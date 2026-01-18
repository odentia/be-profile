from __future__ import annotations

from profile_service.domain.models import Profile, Theme
from profile_service.repo.sql.models import Profiles, Themes


def profile_to_domain(profile_model: Profiles) -> Profile:
    """Преобразование модели БД в доменную сущность"""
    return Profile(
        user_id=profile_model.user_id,
        name=profile_model.name,
        description=profile_model.description,
        avatar_url=profile_model.avatar_url,
        email=profile_model.email,
        created_at=profile_model.created_at,
        updated_at=profile_model.updated_at,
    )


def profile_to_model(profile: Profile) -> Profiles:
    """Преобразование доменной сущности в модель БД"""
    return Profiles(
        user_id=profile.user_id,
        name=profile.name,
        description=profile.description,
        avatar_url=profile.avatar_url,
        email=profile.email,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
    )


def theme_to_domain(theme_model: Themes) -> Theme:
    """Преобразование модели БД в доменную сущность"""
    return Theme(
        user_id=theme_model.user_id,
        backgroundColor=theme_model.backgroundColor,
        backgroundColorMain=theme_model.backgroundColorMain,
        backgroundColorSub=theme_model.backgroundColorSub,
        boxShadow=theme_model.boxShadow,
        danger=theme_model.danger,
        border=theme_model.border,
        subtext=theme_model.subtext,
        text=theme_model.text,
        attention=theme_model.attention,
        glowColor=theme_model.glowColor,
        glowOpacity=theme_model.glowOpacity,
        cards=theme_model.cards,
        circleColor=theme_model.circleColor,
        updated_at=theme_model.updated_at,
    )


def theme_to_model(theme: Theme) -> Themes:
    """Преобразование доменной сущности в модель БД"""
    return Themes(
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
        updated_at=theme.updated_at,
    )
