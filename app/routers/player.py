from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import ApplicationException
from app.config.connection import get_db
from app.services.player import (
    create_player,
    change_player,
    archive_player,
    restore_player,
    get_player_list,
    get_player_id,
    check_player_tg_id,
    get_leaderboard,
    get_my_table,
)
from app.schemas.player import (
    PlayerResponse,
    PlayerAddRequest,
    PlayerPatchRequest,
    LeaderBoardListResponse,
    MyTableResponse,
)
from app.schemas.common import BaseShortResponse, BaseListResponse, ResultResponse


player_router = APIRouter()


@player_router.get("/players", response_model=BaseListResponse)
async def get_player_list_router(
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_player_list(session=session, limit=limit, offset=offset)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@player_router.get("/players/leaderboard", response_model=LeaderBoardListResponse)
async def get_leaderboard_router(
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=20, le=100),
    offset: int = Query(default=0),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_leaderboard(session=session, limit=limit, offset=offset)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        print(f"EEEEE {e}")
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@player_router.get("/players/me", response_model=PlayerResponse)
async def get_player_me_router(
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await get_player_id(session, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")
    

@player_router.get("/players/{id}", response_model=PlayerResponse)
async def get_player_router(
    id: int,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_player_id(session, id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@player_router.get("/players/me/table", response_model=MyTableResponse)
async def get_my_table_router(
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await get_my_table(session, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")
    
    
@player_router.get("/players/tg/{tg_id}", response_model=BaseShortResponse)
async def get_player_tg_router(
    tg_id: int,
    session: AsyncSession = Depends(get_db),
):
    try:
        return await check_player_tg_id(session, tg_id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@player_router.patch("/players/{id}", response_model=ResultResponse)
async def change_player_router(
    id: int,
    item: PlayerPatchRequest,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await change_player(session, id, item, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@player_router.post("/players/{tg_id}", response_model=BaseShortResponse)
async def create_player_router(
    tg_id: int,
    item: PlayerAddRequest,
    session: AsyncSession = Depends(get_db),
):
    try:
        return await create_player(session, item, tg_id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__} - {e}")


@player_router.delete("/players/{id}", response_model=BaseShortResponse)
async def archive_player_router(
    id: int,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await archive_player(session, id, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__} - {e}")


@player_router.post("/players/{id}/restore", response_model=BaseShortResponse)
async def restore_player_router(
    id: int,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await restore_player(session, id, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__} - {e}")



