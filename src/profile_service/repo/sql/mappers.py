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
        updated_at=profile_model.updated_at
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
        updated_at=profile.updated_at
    )


def theme_to_domain(theme_model: Themes) -> Theme:
    """Преобразование модели БД в доменную сущность"""
    return Theme(
        user_id=theme_model.user_id,
        text_color=theme_model.text_color,
        main_bg_color=theme_model.main_bg_color,
        second_bg_color=theme_model.second_bg_color,
        contrast_color=theme_model.contrast_color,
        highlight_color=theme_model.highlight_color,
        blur_transparency=theme_model.blur_transparency,
        updated_at=theme_model.updated_at
    )


def theme_to_model(theme: Theme) -> Themes:
    """Преобразование доменной сущности в модель БД"""
    return Themes(
        user_id=theme.user_id,
        text_color=theme.text_color,
        main_bg_color=theme.main_bg_color,
        second_bg_color=theme.second_bg_color,
        contrast_color=theme.contrast_color,
        highlight_color=theme.highlight_color,
        blur_transparency=theme.blur_transparency,
        updated_at=theme.updated_at
    )

