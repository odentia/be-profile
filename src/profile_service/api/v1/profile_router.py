from __future__ import annotations

from fastapi import APIRouter, HTTPException, status, Depends, Request

from profile_service.dtos.http import (
    ProfileUpdateRequest, ProfileResponse,
    ThemeUpdateRequest, ThemeResponse,
    ThemeImportRequest,
    PasswordChangeRequest, DeleteAccountRequest
)
from profile_service.domain.services import ProfileService, ThemeService, PasswordService
from profile_service.api.deps import (
    get_profile_repo, get_theme_repo, get_password_service, get_current_user_id, get_event_publisher
)

# Создаем роутер для профиля
profile_router = APIRouter(prefix="/profile", tags=["Profile"])


@profile_router.get("/me", response_model=ProfileResponse)
async def get_profile(
    request: Request,
    profile_repo=Depends(get_profile_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Получить профиль текущего пользователя"""
    user_id = await get_current_user_id(request)
    service = ProfileService(profile_repo, event_publisher)
    result = await service.get_profile(user_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return result


@profile_router.put("/me", response_model=ProfileResponse)
async def update_profile(
    request_data: ProfileUpdateRequest,
    request: Request,
    profile_repo=Depends(get_profile_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Обновить профиль текущего пользователя"""
    user_id = await get_current_user_id(request)
    service = ProfileService(profile_repo, event_publisher)
    result = await service.update_profile(user_id, request_data)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return result


@profile_router.get("/theme", response_model=ThemeResponse)
async def get_theme(
    request: Request,
    theme_repo=Depends(get_theme_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Получить тему текущего пользователя"""
    user_id = await get_current_user_id(request)
    service = ThemeService(theme_repo, event_publisher)
    result = await service.get_theme(user_id)
    
    return result


@profile_router.put("/theme", response_model=ThemeResponse)
async def update_theme(
    request_data: ThemeUpdateRequest,
    request: Request,
    theme_repo=Depends(get_theme_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Обновить тему текущего пользователя"""
    user_id = await get_current_user_id(request)
    service = ThemeService(theme_repo, event_publisher)
    result = await service.update_theme(user_id, request_data)
    
    return result


@profile_router.get("/theme/{user_id}", response_model=ThemeResponse)
async def get_theme_by_user_id(
    user_id: str,
    theme_repo=Depends(get_theme_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Получить тему пользователя по его ID (публичный endpoint)"""
    service = ThemeService(theme_repo, event_publisher)
    result = await service.get_theme_by_user_id(user_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Theme not found"
        )
    
    return result


@profile_router.post("/theme/import", response_model=ThemeResponse)
async def import_theme(
    request_data: ThemeImportRequest,
    request: Request,
    theme_repo=Depends(get_theme_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Импортировать тему от другого пользователя в свой профиль"""
    target_user_id = await get_current_user_id(request)
    service = ThemeService(theme_repo, event_publisher)
    result = await service.import_theme(target_user_id, request_data.user_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source theme not found"
        )
    
    return result


@profile_router.post("/change-password")
async def change_password(
    request_data: PasswordChangeRequest,
    request: Request,
    password_service=Depends(get_password_service)
):
    """Изменить пароль пользователя"""
    user_id = await get_current_user_id(request)
    # TODO: Интеграция с auth-service через clients/auth_client.py
    # auth_client = get_auth_client()
    # success = await auth_client.change_password(user_id, request_data.current_password, request_data.new_password)
    
    return {"message": "Password change requested. Integration with auth-service needed."}


@profile_router.delete("/account")
async def delete_account(
    request_data: DeleteAccountRequest,
    request: Request,
    profile_repo=Depends(get_profile_repo),
    theme_repo=Depends(get_theme_repo),
    event_publisher=Depends(get_event_publisher)
):
    """Удалить аккаунт пользователя"""
    user_id = await get_current_user_id(request)
    # TODO: Интеграция с auth-service для проверки пароля
    # auth_client = get_auth_client()
    # verified = await auth_client.verify_password(user_id, request_data.password)
    
    profile_service = ProfileService(profile_repo, event_publisher)
    success = await profile_service.delete_profile(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete account"
        )
    
    return {"message": "Account deleted successfully"}

