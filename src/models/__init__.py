import enum
from datetime import datetime, timezone
from typing import List, Optional

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
    city: Mapped[Optional[str]] = mapped_column(Text)
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
    slug: Mapped[str] = mapped_column(Text)
    start_at: Mapped[datetime] = mapped_column(DateTime)
    state: Mapped[ActivityState] = mapped_column(Enum(ActivityState))

    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournament.id"), init=False
    )
    tournament: Mapped["TournamentDB"] = relationship(
        back_populates="events", init=False
    )

    sets: Mapped[List["SetDB"]] = relationship(
        back_populates="event", init=False
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


class SetDB(Base):
    __tablename__ = "set"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    winner_seed: Mapped[int] = mapped_column(Integer)
    loser_seed: Mapped[int] = mapped_column(Integer)

    winner_score: Mapped[int] = mapped_column(Integer)
    loser_score: Mapped[int] = mapped_column(Integer)

    winner_player_id: Mapped[int] = mapped_column(
        ForeignKey("player.id"), init=False
    )
    winner_player: Mapped["PlayerDB"] = relationship(
        back_populates="winning_sets",
        foreign_keys=[winner_player_id]
    )

    loser_player_id: Mapped[int] = mapped_column(
        ForeignKey("player.id"), init=False
    )
    loser_player: Mapped["PlayerDB"] = relationship(
        back_populates="losing_sets",
        foreign_keys=[loser_player_id]
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("event.id"), index=True, init=False
    )
    event: Mapped["EventDB"] = relationship(
        back_populates="sets"
    )

    def __repr__(self) -> str:
        return f"SetDB(id={self.id!r})"


class PlayerDB(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gamer_tag: Mapped[str] = mapped_column(Text)

    winning_sets: Mapped[List["SetDB"]] = relationship(
        back_populates="winner_player",
        foreign_keys="SetDB.winner_player_id",
        init=False
    )
    losing_sets: Mapped[List["SetDB"]] = relationship(
        back_populates="loser_player",
        foreign_keys="SetDB.loser_player_id",
        init=False
    )

    def __repr__(self) -> str:
        return f"PlayerDB(id={self.id!r}, gamer_tag={self.gamer_tag!r})"
