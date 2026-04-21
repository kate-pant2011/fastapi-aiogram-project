from .base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship


class Player(BaseModel):
    __tablename__ = "players"

    name = Column(String, nullable=False, unique=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    elo = Column(Float, default=0)

    is_archived = Column(Boolean, nullable=False, default=False, index=True)

    games = relationship("GamePlayer", back_populates="player")

    organized_games = relationship("Game", back_populates="organizer")
    table_participations = relationship("TablePlayer", back_populates="player")
    
    eliminations = relationship("TablePlayer", back_populates="eliminator")
    elo_history = relationship("EloHistory", back_populates="player")



