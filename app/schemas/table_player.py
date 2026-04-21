from pydantic import BaseModel, ConfigDict, Field
from .common import BaseShortResponse
from .table import TableShortResponse
from datetime import datetime
from typing import Literal


class TablePlayerShort(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TablePlayerResponse(BaseModel):
    id: int
    player: BaseShortResponse
    table: TableShortResponse
    started_at: datetime
    finished_at: datetime | None
    is_active: bool
    position: int | None
    chips: int
    table_participants: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TablePlayerPatch(BaseModel):
    chips: int | None = Field(None, ge=0)
    eliminated: Literal[True] | None = None

    model_config = {"extra": "forbid"}
