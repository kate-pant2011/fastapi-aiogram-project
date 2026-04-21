from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import ApplicationException
from app.config.connection import get_db
from app.services.table import (
    create_tables,
    delete_table,
    get_table_list,
    get_table_id,
    change_table,
)
from app.schemas.table import TableListResponse, TableResponse, TablesAddRequest, TablePatchRequest
from app.schemas.common import ResultResponse
from app.services.player import check_player_tg_id


table_router = APIRouter()


@table_router.get("/games/{game_id}/tables", response_model=TableListResponse)
async def get_table_list_router(
    game_id: int,
    tg_id: int = Query(description="checking active player"),
    organizer_id: int | None = Query(default=None),
    session: AsyncSession = Depends(get_db),
    limit: int = Query(default=50, le=100),
    offset: int = Query(default=0),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_table_list(session=session, limit=limit, offset=offset, game_id=game_id, organizer_id=organizer_id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@table_router.get("/tables/{id}", response_model=TableResponse)
async def get_table_router(
    id: int,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        await check_player_tg_id(session, tg_id)
        return await get_table_id(session, id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")


@table_router.post("/games/{game_id}/tables", response_model=ResultResponse)
async def create_tables_router(
    game_id: int,
    item: TablesAddRequest,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await create_tables(session, item, game_id, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__} - {e}")


@table_router.delete("/tables/{table_id}", response_model=ResultResponse)
async def delete_tables_router(
    table_id: int,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await delete_table(session, table_id, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail=e.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__} - {e}")


@table_router.patch("/tables/{id}", response_model=TableResponse)
async def change_player_router(
    id: int,
    item: TablePatchRequest,
    tg_id: int = Query(description="checking active player"),
    session: AsyncSession = Depends(get_db),
):
    try:
        user = await check_player_tg_id(session, tg_id)
        return await change_table(session, id, item, user.id)

    except ApplicationException as e:
        raise HTTPException(status_code=e.code, detail={"message": e.name, "payload": e.payload})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f" {type(e).__name__} - {e}")
