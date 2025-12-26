import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import (DeclarativeBase, Mapped, MappedAsDataclass,
                            mapped_column, relationship)
from sqlalchemy.sql import func


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
        back_populates="tournament",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    imported: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"TournamentDB(id={self.id!r}, name={self.name!r})"


class EventDB(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text)
    num_entrants: Mapped[int] = mapped_column(Integer)
    slug: Mapped[str] = mapped_column(Text)
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    state: Mapped[ActivityState] = mapped_column(Enum(ActivityState))

    tournament_id: Mapped[int] = mapped_column(
        ForeignKey("tournament.id", ondelete="CASCADE"), init=False
    )
    tournament: Mapped["TournamentDB"] = relationship(
        back_populates="events", init=False
    )

    sets: Mapped[List["SetDB"]] = relationship(
        back_populates="event", init=False,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    imported: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"EventDB(id={self.id!r}, name={self.name!r})"


class SetDB(Base):
    __tablename__ = "set"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    winner_seed: Mapped[int] = mapped_column(Integer)
    loser_seed: Mapped[int] = mapped_column(Integer)

    winner_score: Mapped[int] = mapped_column(Integer)
    loser_score: Mapped[int] = mapped_column(Integer)

    winner_team_id: Mapped[int] = mapped_column(
        ForeignKey("team.id"), init=False
    )
    winner_team: Mapped["TeamDB"] = relationship(
        back_populates="winning_sets",
        foreign_keys=[winner_team_id]
    )

    loser_team_id: Mapped[int] = mapped_column(
        ForeignKey("team.id"), init=False
    )
    loser_team: Mapped["TeamDB"] = relationship(
        back_populates="losing_sets",
        foreign_keys=[loser_team_id]
    )

    event_id: Mapped[int] = mapped_column(
        ForeignKey("event.id", ondelete="CASCADE"), index=True, init=False
    )
    event: Mapped["EventDB"] = relationship(
        back_populates="sets"
    )

    def __repr__(self) -> str:
        return f"SetDB(id={self.id!r})"


team_player = Table(
    "team_player",
    Base.metadata,
    Column("team_id", ForeignKey("team.id"), primary_key=True, index=True),
    Column("player_id", ForeignKey("player.id"), primary_key=True, index=True),
)


class TeamDB(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, autoincrement=True
    )

    players: Mapped[List["PlayerDB"]] = relationship(
        secondary=team_player,
        back_populates="teams",
        init=False
    )

    winning_sets: Mapped[List["SetDB"]] = relationship(
        back_populates="winner_team",
        foreign_keys="SetDB.winner_team_id",
        init=False
    )
    losing_sets: Mapped[List["SetDB"]] = relationship(
        back_populates="loser_team",
        foreign_keys="SetDB.loser_team_id",
        init=False
    )

    def __repr__(self) -> str:
        return f"TeamDB(id={self.id!r})"


class PlayerDB(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    gamer_tag: Mapped[str] = mapped_column(Text)

    teams: Mapped[List["TeamDB"]] = relationship(
        secondary=team_player,
        back_populates="players",
        init=False
    )

    def __repr__(self) -> str:
        return f"PlayerDB(id={self.id!r}, gamer_tag={self.gamer_tag!r})"
