from __future__ import annotations

from typing import Optional
# TODO: Использовать common-http
# from common_http import HttpClient


class AuthClient:
    """HTTP клиент для auth-service"""

    def __init__(self, base_url: str):
        # TODO: Инициализировать через common-http
        # self.client = HttpClient(base_url=base_url)
        self.base_url = base_url

    async def verify_token(self, token: str) -> Optional[dict]:
        """Проверить JWT токен"""
        # TODO: Реализовать через common-http
        # return await self.client.get("/api/v1/auth/verify", headers={"Authorization": f"Bearer {token}"})
        pass

    async def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Изменить пароль пользователя"""
        # TODO: Реализовать через common-http
        # return await self.client.post("/api/v1/auth/change-password", json={...})
        pass

    async def delete_user(self, user_id: str, password: str) -> bool:
        """Удалить пользователя"""
        # TODO: Реализовать через common-http
        # return await self.client.delete(f"/api/v1/auth/users/{user_id}", json={"password": password})
        pass
