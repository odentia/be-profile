from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from profile_service.core.config import Settings
from profile_service.core.db import init_engine, close_engine, init_session_factory
from profile_service.core.logging import get_logger

log = get_logger(__name__)


def build_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # --- Startup ---
        log.info("Starting service...", extra={"app": settings.app_name, "env": settings.env})

        # DB engine & session factory
        engine = await init_engine(settings.database_url, echo=settings.sql_echo)
        sf = init_session_factory(engine)
        app.state.engine = engine
        app.state.session_factory = sf
        app.state.ready = True
        log.info("Service is up")

        try:
            yield
        finally:
            # --- Shutdown ---
            log.info("Shutting down service...")
            app.state.ready = False

            # Close DB engine
            await close_engine(engine)

            log.info("Bye")

    return lifespan

