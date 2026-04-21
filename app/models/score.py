from .base import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship


class EloHistory(BaseModel):
    __tablename__ = "elo_history"

    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    player = relationship("Player", back_populates="elo_history")

    game_id = Column(Integer, ForeignKey("games.id"), nullable=False, index=True)
    game = relationship("Game", back_populates="elo_history")

    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False, index=True)
    table = relationship("Table", back_populates="elo_history")

    elo_before = Column(Float, nullable=False)
    elo_after = Column(Float, nullable=False, default=0)
    elo_change = Column(Float, nullable=True)

    bounty_bonus = Column(Float, nullable=True)
    players_total = Column(Integer)
    position = Column(Integer)
    chips = Column(Integer, nullable=False, default=0)
