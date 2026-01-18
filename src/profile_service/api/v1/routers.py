from fastapi import APIRouter

from profile_service.api.v1.profile_router import profile_router

api_v1 = APIRouter(prefix="/v1", tags=["v1"])

# Включаем роутер профиля
api_v1.include_router(profile_router)


@api_v1.get("/healthz")
async def healthz():
    return {"status": "ok"}
