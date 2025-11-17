# profile-service

Сервис профиля пользователя для микросервисной архитектуры.

## Описание

Этот сервис отвечает за:
- Управление профилями пользователей
- Настройку тем пользователей
- Изменение пароля
- Удаление аккаунта

## Технологии

- FastAPI - веб-фреймворк
- SQLAlchemy - ORM
- PostgreSQL - база данных
- Alembic - миграции БД
- JWT - проверка токенов (интеграция с auth-service)

## Установка и запуск

### 1. Установка зависимостей

```bash
uv sync
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/profile_db
ALEMBIC_DATABASE_URL=postgresql://user:password@localhost:5432/profile_db

# JWT Configuration (должен совпадать с auth-service)
JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256

# Application
APP_NAME=profile-service
APP_VERSION=0.1.0
ENV=dev
ENABLE_DOCS=true

# HTTP
HTTP_HOST=0.0.0.0
HTTP_PORT=8001
RELOAD=false

# CORS
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:8080

# Logging
LOG_LEVEL=INFO
```

### 3. Запуск миграций

```bash
uv run alembic upgrade head
```

### 4. Запуск сервиса

```bash
uv run python -m profile_service.api
```

## API Endpoints

### Профиль

- `GET /api/v1/profile/me` - Получить профиль текущего пользователя
- `PUT /api/v1/profile/me` - Обновить профиль

### Тема

- `GET /api/v1/profile/theme` - Получить тему пользователя
- `PUT /api/v1/profile/theme` - Обновить тему

### Безопасность

- `POST /api/v1/profile/change-password` - Изменить пароль
- `DELETE /api/v1/profile/account` - Удалить аккаунт

### Системные

- `GET /api/v1/healthz` - Проверка здоровья сервиса

## Архитектура

Сервис построен по принципам Clean Architecture:

- **domain/** - бизнес-логика и сущности (models, repositories, services, events)
- **dtos/** - HTTP схемы (http.py) и схемы событий (events.py)
- **repo/sql/** - SQLAlchemy модели и репозитории
- **mq/** - работа с message queue (consumer, publisher)
- **clients/** - HTTP клиенты к другим сервисам
- **api/** - HTTP endpoints и middleware
- **core/** - конфигурация, логирование, БД

## Интеграция

Сервис интегрируется с:
- **auth-service** - для проверки JWT токенов и изменения пароля

