from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import ApplicationException
from app.config.connection import get_db
from app.services.score import get_player_elo_history, get_game_rating, close_table_and_update_elo
from app.schemas.score import EloListResponse, RatingListResponse, TableResultResponse
from app.services.player import check_player_tg_id

elo_router = APIRouter()


@elo_router.get("/elo/players/{player_id}", response_model=EloListResponse)
async def get_player_elo_history_router(
    player_id: int,
    tg_id: int = Query("active_player_check"),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_player_elo_history(session, player_id, limit, offset)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)


@elo_router.get("/elo/games/{game_id}/rating", response_model=RatingListResponse)
async def get_game_rating_router(
    game_id: int,
    tg_id: int = Query("active_player_check"),
    session: AsyncSession = Depends(get_db),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_game_rating(session, game_id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)


@elo_router.post("/elo/tables/{table_id}/close", response_model=TableResultResponse)
async def close_table_router(
    table_id: int,
    tg_id: int = Query("active_player_check"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await close_table_and_update_elo(session, table_id, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)
