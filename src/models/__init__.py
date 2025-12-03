import enum
from datetime import datetime, timezone
from typing import List

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column, relationship)


class ActivityState(enum.Enum):
    """enum ActivityState
    CREATED: Activity is created
    ACTIVE: Activity is active or in progress
    COMPLETED: Activity is done
    READY: Activity is ready to be started
    INVALID: Activity is invalid
    CALLED: Activity, like a set, has been called to start
    QUEUED: Activity is queued to run
    """
    CREATED = "CREATED",
    ACTIVE = "ACTIVE",
    COMPLETED = "COMPLETED",
    READY = "READY",
    INVALID = "INVALID",
    CALLED = "CALLED",
    QUEUED = "QUEUED"


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class TournamentDB(Base):
    __tablename__ = "tournament"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(Text)
    country_code: Mapped[str] = mapped_column(Text)
    addr_state: Mapped[str] = mapped_column(Text)

    events: Mapped[List["EventDB"]] = relationship(
        back_populates="tournament"
    )

    imported: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"TournamentDB(id={self.id!r}, name={self.name!r})"


class EventDB(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text)
    num_entrants: Mapped[int] = mapped_column(Integer)
    start_at: Mapped[datetime] = mapped_column(DateTime)

    slug: str
    state: ActivityState

    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournament.id"), init=False
    )
    tournament: Mapped["TournamentDB"] = relationship(
        back_populates="events", init=False
    )

    imported: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )

    def __repr__(self) -> str:
        return f"EventDB(id={self.id!r}, name={self.name!r})"
