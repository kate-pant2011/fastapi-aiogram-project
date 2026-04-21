from .base import BaseModel
from sqlalchemy import Column, Boolean, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship


class TablePlayer(BaseModel):
    __tablename__ = "table_players"

    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    player = relationship("Player", back_populates="table_participations")

    table_id = Column(
        Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False, index=True
    )
    table = relationship("Table", back_populates="table_participants")

    started_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    position = Column(Integer, nullable=True)
    chips = Column(Integer, nullable=False, default=0)

    eliminated_by_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    eliminator = relationship(
        "Player", foreign_keys=[eliminated_by_id], back_populates="eliminations"
    )

    __table_args__ = (UniqueConstraint("table_id", "player_id"),)
