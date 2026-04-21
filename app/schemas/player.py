from pydantic import BaseModel, ConfigDict, Field
from .common import BaseShortResponse
from .table_player import TablePlayerShort


class PlayerResponse(BaseModel):
    id: int
    telegram_id: int
    name: str
    elo: float
    player_games: list[BaseShortResponse] | None = None
    organized_games: list[BaseShortResponse] | None

    total_games: int = 0
    total_knockouts: int = 0

    model_config = ConfigDict(from_attributes=True)


class LeaderboardResponse(BaseModel):
    id: int
    name: str
    elo: float


class LeaderBoardListResponse(BaseModel):
    items: list[LeaderboardResponse]
    total: int
    limit: int
    offset: int


class PlayerPatchRequest(BaseModel):
    name: str | None = Field(None, min_length=1)

    model_config = {"extra": "forbid"}


class PlayerAddRequest(BaseModel):
    name: str = Field(min_length=1)

    model_config = {"extra": "forbid"}


class PlayerRatingReponse(BaseModel):
    ratings: dict[str, int]


from typing import Literal


class TablePlayerInfo(BaseModel):
    id: int
    name: str
    chips: int


class MyTableResponse(BaseModel):
    scope: Literal["table", "game"]

    table_id: int | None = None
    table_number: int | None = None

    players: list[TablePlayerInfo]
