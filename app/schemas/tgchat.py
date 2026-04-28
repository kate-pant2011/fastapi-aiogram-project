from pydantic import BaseModel, ConfigDict, Field


class TgchatShortResponse(BaseModel):
    chat_title: str
    chat_id: int
    thread_id: int

    model_config = ConfigDict(from_attributes=True)


class TgchatListResponse(BaseModel):
    items: list[TgchatShortResponse]
    total: int
    limit: int
    offset: int


class TgchatAddRequest(BaseModel):
    chat_id: int 
    thread_id: int 
    chat_title: str

    model_config = {"extra": "forbid"}