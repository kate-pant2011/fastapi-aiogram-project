from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import ApplicationException
from app.config.connection import get_db
from app.services.tgchat import (
    create_tgchat,
    get_tgchat_id,
    get_tgchat_list
)
from app.schemas.tgchat import TgchatAddRequest, TgchatListResponse, TgchatShortResponse
from app.schemas.common import ResultResponse
from app.services.player import check_player_tg_id


tgchat_router = APIRouter()



@tgchat_router.get("/tgchats", response_model=TgchatListResponse)
async def get_tgchat_list_router(
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_tgchat_list(session=session, limit=limit, offset=offset)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")

@tgchat_router.get("/tgchats/{chat_id}", response_model=TgchatShortResponse)
async def get_tgchat_router(
    chat_id: int,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_tgchat_id(session, chat_id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")



@tgchat_router.post("/tgchats", response_model=ResultResponse)
async def create_tgchats_router(
    item: TgchatAddRequest,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await create_tgchat(session, item, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__} - {e}")