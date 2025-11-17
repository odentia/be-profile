# Структура микросервиса профиля

## Структура файлов

```
profile-service/
├── src/
│   └── profile_service/
│       ├── domain/                    # Доменный слой
│       │   ├── models.py             # Доменные модели (Profile, Theme)
│       │   ├── repositories.py      # Интерфейсы репозиториев
│       │   ├── services.py          # Бизнес-логика (ProfileService, ThemeService)
│       │   └── events.py            # События для публикации
│       ├── dtos/                     # Data Transfer Objects
│       │   ├── http.py              # HTTP схемы (запросы/ответы)
│       │   └── events.py            # Схемы событий
│       ├── repo/                     # Репозитории
│       │   └── sql/
│       │       ├── models.py         # SQLAlchemy модели
│       │       ├── repositories.py   # Реализация репозиториев
│       │       ├── mappers.py        # Преобразование данных
│       │       └── interfaces.py     # Интерфейсы
│       ├── mq/                       # Message Queue
│       │   ├── consumer.py          # Обработка событий
│       │   └── publisher.py         # Публикация событий
│       ├── clients/                  # HTTP клиенты
│       │   └── auth_client.py       # Клиент для auth-service
│       ├── api/                      # API слой
│       │   ├── app.py               # FastAPI приложение
│       │   ├── __main__.py          # Точка входа
│       │   ├── lifespan.py          # Управление жизненным циклом
│       │   ├── deps.py              # Dependency injection
│       │   └── v1/
│       │       ├── routers.py       # Основной роутер
│       │       └── profile_router.py # Роутер профиля
│       └── core/                     # Утилиты
│           ├── config.py            # Настройки (TODO: common-config)
│           ├── logging.py           # Логирование (TODO: common-logging)
│           └── db.py                # Подключение к БД
├── alembic/                          # Миграции БД
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── infra/
│   └── docker/
│       └── Dockerfile
├── pyproject.toml
├── alembic.ini
├── Makefile
├── README.md
└── .env.example
```

## Зависимости

### Текущие (временные):
- Прямые зависимости в `pyproject.toml`

### Планируемые (из common-* пакетов):
- `myorg-contracts>=1.2,<2.0` - схемы HTTP и событий
- `myorg-common-config>=0.6,<0.7` - настройки
- `myorg-common-logging>=0.6,<0.7` - логирование
- `myorg-common-http>=0.6,<0.7` - HTTP клиенты
- `myorg-common-mq>=0.6,<0.7` - message queue

## TODO для интеграции

1. **contracts**: Заменить локальные DTO на импорты из `contracts.http.profile` и `contracts.events.profile_v1`
2. **common-config**: Использовать `BaseSettings` из `common-config`
3. **common-logging**: Использовать `init_logging` из `common-logging`
4. **common-http**: Использовать `HttpClient` в `clients/auth_client.py`
5. **common-mq**: Использовать `MessagePublisher` и `MessageConsumer` в `mq/`

