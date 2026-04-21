from .base import BaseModel
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Enum as SQLEnum,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.orm import relationship
from enum import Enum


class Status(str, Enum):
    JOINED = "joined"
    LEFT = "left"


class GameStatus(str, Enum):
    AWAITED = "awaited"
    IN_ACTION = "in_action"
    CANCELED = "canceled"


class Game(BaseModel):
    __tablename__ = "games"

    name = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=True)
    status = Column(
        SQLEnum(GameStatus, name="game_status"),
        nullable=False,
        default=GameStatus.AWAITED,
    )
    is_archived = Column(Boolean, nullable=False, default=False, index=True)

    players = relationship("GamePlayer", back_populates="game")

    organizer_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    organizer = relationship("Player", back_populates="organized_games")

    tables = relationship("Table", back_populates="game")
    elo_history = relationship("EloHistory", back_populates="game")


class GamePlayer(BaseModel):
    __tablename__ = "game_players"

    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player = relationship("Player", back_populates="games")

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    game = relationship("Game", back_populates="players")

    status = Column(
        SQLEnum(Status, name="game_player_status"),
        nullable=False,
        default=Status.JOINED,
    )

    __table_args__ = (UniqueConstraint("player_id", "game_id"),)
