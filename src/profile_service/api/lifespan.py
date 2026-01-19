import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from profile_service.core.config import Settings
from profile_service.core.db import (
    init_engine,
    close_engine,
    init_session_factory,
    get_session_factory,
)
from profile_service.core.logging import get_logger
from profile_service.mq.consumer import EventConsumer
from profile_service.mq.publisher import EventPublisher
from profile_service.domain.models import Profile
from profile_service.repo.sql.repositories import SQLProfileRepository

log = get_logger(__name__)


async def handle_user_created(event_data: dict):
    """Обработчик события создания пользователя"""
    try:
        user_id = event_data.get("user_id") or event_data.get("userId")
        name = event_data.get("name") or event_data.get("username") or "User"
        email = event_data.get("email") or ""

        if not user_id:
            log.warning(f"Invalid event data for user_created: {event_data}")
            return

        session_factory = get_session_factory()
        if not session_factory:
            log.error("Session factory not initialized")
            return

        async with session_factory() as session:
            try:
                profile_repo = SQLProfileRepository(session)

                # Проверяем, не существует ли уже профиль
                existing_profile = await profile_repo.get_by_user_id(user_id)
                if existing_profile:
                    log.info(f"Profile already exists for user {user_id}")
                    return

                # Создаем новый профиль
                new_profile = Profile(user_id=user_id, name=name, email=email)

                await profile_repo.create(new_profile)
                log.info(f"Profile created for user {user_id}")

            except Exception as e:
                await session.rollback()
                log.error(f"Error creating profile for user {user_id}: {e}")
                raise

    except Exception as e:
        log.error(f"Error handling user_created event: {e}")


async def handle_user_deleted(event_data: dict):
    """Обработчик события удаления пользователя"""
    try:
        user_id = event_data.get("user_id") or event_data.get("userId")

        if not user_id:
            log.warning(f"Invalid event data for user_deleted: {event_data}")
            return

        session_factory = get_session_factory()
        if not session_factory:
            log.error("Session factory not initialized")
            return

        async with session_factory() as session:
            try:
                profile_repo = SQLProfileRepository(session)
                deleted = await profile_repo.delete(user_id)

                if deleted:
                    log.info(f"Profile deleted for user {user_id}")
                else:
                    log.warning(f"Profile not found for user {user_id}")

            except Exception as e:
                await session.rollback()
                log.error(f"Error deleting profile for user {user_id}: {e}")
                raise

    except Exception as e:
        log.error(f"Error handling user_deleted event: {e}")


async def start_consumer(consumer: EventConsumer):
    """Запуск consumer в фоновом режиме"""
    try:
        await consumer.start_consuming()
    except asyncio.CancelledError:
        log.info("Consumer cancelled")
    except Exception as e:
        log.error(f"Consumer error: {e}")


def build_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # --- Startup ---
        log.info("Starting service...", extra={"app": settings.app_name, "env": settings.env})
        consumer_task = None

        try:
            # DB engine & session factory
            engine = await init_engine(settings.database_url, echo=settings.sql_echo)
            sf = init_session_factory(engine)
            app.state.engine = engine
            app.state.session_factory = sf

            # Initialize event publisher с retry
            publisher = None
            max_retries = 5
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    publisher = EventPublisher(settings)
                    await publisher.connect()
                    app.state.event_publisher = publisher
                    log.info("Event publisher initialized successfully")
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        log.warning(
                            f"Failed to connect event publisher to RabbitMQ (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s..."
                        )
                        await asyncio.sleep(retry_delay)
                    else:
                        log.error(
                            f"Failed to connect event publisher to RabbitMQ after {max_retries} attempts: {e}. Events will not be published."
                        )
                        app.state.event_publisher = None

            # Initialize event consumer с retry
            consumer = None
            consumer_task = None

            for attempt in range(max_retries):
                try:
                    consumer = EventConsumer(settings)
                    await consumer.connect()

                    # Регистрируем обработчики событий
                    consumer.register_handler("user_created", handle_user_created)
                    consumer.register_handler("user_deleted", handle_user_deleted)

                    # Запускаем consumer в фоновой задаче
                    consumer_task = asyncio.create_task(start_consumer(consumer))
                    app.state.consumer = consumer
                    app.state.consumer_task = consumer_task
                    log.info("Event consumer started successfully")
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        log.warning(
                            f"Failed to connect event consumer to RabbitMQ (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {retry_delay}s..."
                        )
                        await asyncio.sleep(retry_delay)
                    else:
                        log.error(
                            f"Failed to connect event consumer to RabbitMQ after {max_retries} attempts: {e}. Events will not be consumed."
                        )
                        app.state.consumer = None
                        app.state.consumer_task = None

            app.state.ready = True
            log.info("Service is up")

        except Exception as e:
            log.error(f"Failed to start service: {e}")
            raise

        try:
            yield
        finally:
            # --- Shutdown ---
            log.info("Shutting down service...")
            app.state.ready = False

            # Останавливаем consumer
            if hasattr(app.state, "consumer_task") and app.state.consumer_task:
                app.state.consumer_task.cancel()
                try:
                    await app.state.consumer_task
                except asyncio.CancelledError:
                    pass

            if hasattr(app.state, "consumer") and app.state.consumer:
                try:
                    await app.state.consumer.close()
                    log.info("Event consumer closed")
                except Exception as e:
                    log.warning(f"Error closing consumer: {e}")

            # Close event publisher
            if hasattr(app.state, "event_publisher") and app.state.event_publisher:
                try:
                    await app.state.event_publisher.close()
                    log.info("Event publisher closed")
                except Exception as e:
                    log.warning(f"Error closing publisher: {e}")

            # Close DB engine
            await close_engine()

            log.info("Bye")

    return lifespan
