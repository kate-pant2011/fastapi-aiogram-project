from pydantic import BaseModel, ConfigDict, Field
from .common import BaseShortResponse
from .table import TableShortResponse
from datetime import datetime


class GameResponse(BaseModel):
    id: int
    name: str
    start_time: datetime | None
    status: str
    organizer: BaseShortResponse
    players: list[BaseShortResponse] | None
    tables: list[TableShortResponse] | None

    model_config = ConfigDict(from_attributes=True)


class GamePatchRequest(BaseModel):
    name: str | None = Field(None, min_length=1)
    is_archived: bool | None = None
    start_time: datetime | None = None

    model_config = {"extra": "forbid"}


class GameAddRequest(BaseModel):
    name: str = Field(min_length=1)
    start_time: datetime

    model_config = {"extra": "forbid"}


class GPPlayerResponse(BaseModel):
    game_id: int
    player: BaseShortResponse
    status: str

    model_config = ConfigDict(from_attributes=True)

class GamePlayerList(BaseModel):
    items: list[GPPlayerResponse]
    total: int
    limit: int
    offset: int


class TablePlayerDistribute(BaseModel):
    id: int
    name: str
    telegram_id: int


class TableDistribute(BaseModel):
    id: int
    number: int
    round: int
    players: list[TablePlayerDistribute]


class DistributeTablesResponse(BaseModel):
    game_id: int
    tables: list[TableDistribute]
