from pydantic import BaseModel, ConfigDict, Field
from .common import BaseShortResponse
from datetime import datetime
from typing import Literal


class TableCountResponse(BaseModel):
    id: int
    number: int
    total_participants: int | None = None

    model_config = ConfigDict(from_attributes=True)


class TableShortResponse(BaseModel):
    id: int
    number: int

    model_config = ConfigDict(from_attributes=True)


class TableListResponse(BaseModel):
    items: list[TableCountResponse]
    total: int
    limit: int
    offset: int


class TableResponse(BaseModel):
    id: int
    number: int
    started_at: datetime | None
    finished_at: datetime | None
    players: list[BaseShortResponse] | None = None
    game: BaseShortResponse

    model_config = ConfigDict(from_attributes=True)


class TablesAddRequest(BaseModel):
    total_tables: int = Field(gt=0)
    round: Literal[1, 2]
    model_config = {"extra": "forbid"}


class TablePatchRequest(BaseModel):
    started_at: datetime | None = None
    finished_at: datetime | None = None
    round: int | None = Field(None, gt=0)

    model_config = {"extra": "forbid"}
