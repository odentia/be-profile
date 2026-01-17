from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Any, TypeVar

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound="Base")


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower()

    def to_dict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def update(self: T, **kwargs) -> T:
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        return self

    async def save(self: T, session: AsyncSession) -> T:
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    async def delete(self, session: AsyncSession) -> None:
        await session.delete(self)
        await session.commit()

    @classmethod
    async def get_by_id(cls: type[T], session: AsyncSession, id: Any) -> T | None:
        return await session.get(cls, id)

    @classmethod
    def from_dict(cls: type[T], data: dict[str, Any]) -> T:
        return cls(**data)


UUIDStr = Annotated[str, mapped_column(UUID(as_uuid=False), primary_key=True)]


class Profiles(Base):
    """Таблица профилей пользователей"""
    user_id: Mapped[UUIDStr] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )


class Themes(Base):
    """Таблица тем пользователей"""
    user_id: Mapped[UUIDStr] = mapped_column(primary_key=True)
    backgroundColor: Mapped[str] = mapped_column(String(50), default="#14141A", nullable=False)
    backgroundColorMain: Mapped[str] = mapped_column(String(50), default="#14141A", nullable=False)
    backgroundColorSub: Mapped[str] = mapped_column(String(50), default="#272A33", nullable=False)
    boxShadow: Mapped[str] = mapped_column(String(100), default="rgba(0, 0, 0, 0.1)", nullable=False)
    danger: Mapped[str] = mapped_column(String(50), default="#ff4444", nullable=False)
    border: Mapped[str] = mapped_column(String(50), default="#272A33", nullable=False)
    subtext: Mapped[str] = mapped_column(String(50), default="#a0a0a0", nullable=False)
    text: Mapped[str] = mapped_column(String(50), default="#ffffff", nullable=False)
    attention: Mapped[str] = mapped_column(String(50), default="#ffaa00", nullable=False)
    glowColor: Mapped[str] = mapped_column(String(50), default="#6C63FF", nullable=False)
    glowOpacity: Mapped[str] = mapped_column(String(10), default="0.3", nullable=False)
    cards: Mapped[str] = mapped_column(String(50), default="#1e1e24", nullable=False)
    circleColor: Mapped[str] = mapped_column(String(50), default="#6C63FF", nullable=False)
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

