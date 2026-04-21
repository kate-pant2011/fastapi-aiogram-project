from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .common import get_all_and_total
from app.models.score import EloHistory
from app.models.player import Player


async def get_elo_history_by_player(session, player_id, limit, offset):
    stmt = (
        select(EloHistory)
        .options(selectinload(EloHistory.player))
        .options(selectinload(EloHistory.game))
        .options(selectinload(EloHistory.table))
        .where(EloHistory.player_id == player_id)
        .order_by(EloHistory.created_at.desc())
    )

    return await get_all_and_total(session, stmt, limit, offset)


async def get_game_players_last_rating(session, game_id):
    subquery = (
        select(
            EloHistory.player_id,
            func.max(EloHistory.id).label("max_id")
        )
        .where(EloHistory.game_id == game_id)
        .group_by(EloHistory.player_id)
        .subquery()
    )

    stmt = (
        select(Player, EloHistory.elo_after)
        .join(subquery, subquery.c.player_id == Player.id)
        .join(EloHistory, EloHistory.id == subquery.c.max_id)
    )

    result = await session.execute(stmt)

    return [
        {"player": row[0], "rating": row[1]}
        for row in result.all()
    ]


async def create_elo_history(session, table_player):
    elo = EloHistory(
        player_id=table_player.player_id,
        game_id=table_player.table.game_id,
        table_id=table_player.table_id,
        elo_before=0,
        elo_after=0,
        elo_change=0,
        players_total=0,
        position=table_player.position,
        chips=table_player.chips,
    )

    session.add(elo)
    await session.flush()