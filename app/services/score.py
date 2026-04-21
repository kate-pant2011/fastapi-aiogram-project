from app.database.score import (
    get_elo_history_by_player,
    get_game_players_last_rating,
    create_elo_history
)
from app.config.config import ApplicationException
from app.schemas.common import to_schema
from app.database.table import get_table_by_id
from app.database.table_player import get_table_players_by_id
from app.schemas.score import EloHistoryResponse
from app.schemas.common import BaseShortResponse
from sqlalchemy.exc import IntegrityError
from datetime import datetime


async def get_player_elo_history(session, player_id, limit, offset):
    result = await get_elo_history_by_player(session, player_id, limit, offset)

    return {
        "items": [to_schema(EloHistoryResponse, e) for e in result.items],
        "total": result.total,
        "limit": limit,
        "offset": offset,
    }


async def get_game_rating(session, game_id):
    players = await get_game_players_last_rating(session, game_id)

    return {
        "items": [
            {
                "player": to_schema(BaseShortResponse, p["player"]),
                "rating": p["rating"],
            }
            for p in players
        ]
    }


async def close_table_and_update_elo(session, table_id, user_id):
    table = await get_table_by_id(session, table_id)

    if not table:
        raise ApplicationException("Table not found", 404)

    if table.game.organizer_id != user_id:
        raise ApplicationException("Only organizer can close table", 400)

    table_players = await get_table_players_by_id(session, table_id)

    if not table_players:
        raise ApplicationException("No players at table", 400)

    # calculate_elo(players)

    elo_results = []

    for tp in table_players:
        player = tp.player

        # add calculation rules
        elo_before = player.elo
        elo_change = 0.0
        bounty_bonus = 0.0
        elo_after = elo_before + elo_change + bounty_bonus

        player.elo = elo_after
        
        elo_history = await create_elo_history(
            session=session,
            player_id=player.id,
            game_id=table.game_id,
            elo_before=elo_before,
            elo_after=elo_after,
            elo_change=elo_change,
            bounty_bonus=bounty_bonus,
            position=tp.position,
            chips=tp.chips,
        )


        tp.is_active = False
        tp.finished_at = datetime.utcnow()

        elo_results.append({
            "player": {
                "id": player.id,
                "name": player.name,
            },
            "game_id": table.game_id,
            "elo_change": elo_change,
            "bounty_bonus": bounty_bonus,
            "position": tp.position,
            "chips": tp.chips,
        })

    table.finished_at = datetime.utcnow()


    elo_results.sort(key=lambda x: x["position"])

    return {
        "id": table.id,
        "number": table.number,
        "game_id": table.game_id,
        "elo_history": elo_results,
    }