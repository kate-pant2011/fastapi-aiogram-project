from app.database.game import (
    get_all_games,
    get_game_by_id,
    add_game,
    add_to_game,
    get_game_players,
    is_player_in_game,
    get_game_players_count,
)
from app.database.table_player import get_active_player_table
from app.config.config import ApplicationException
from app.schemas.common import to_schema
from app.schemas.game import GameResponse, GPPlayerResponse
from app.schemas.common import BaseShortResponse
from datetime import datetime
from app.models.game import Status, GameStatus
from app.database.score import get_elo_history_by_player
from app.database.table import add_tables


async def check_game_by_id(session, id):
    game = await get_game_by_id(session, id)

    if not game:
        raise ApplicationException("game Not found", 404)

    if game.is_archived:
        raise ApplicationException(f"A game '{game.name}' is archived", 400, {"id": game.id})

    return game


async def get_game_list(session, limit, offset, status=None, organizer_id=None):
    games = await get_all_games(session, limit, offset, status, organizer_id)

    return {
        "items": [to_schema(BaseShortResponse, g) for g in games.items],
        "total": games.total,
        "limit": limit,
        "offset": offset,
    }


async def get_game_players_list(session, game_id, limit, offset):
    game_players = await get_game_players(session, game_id, limit, offset)

    return {
        "items": [to_schema(GPPlayerResponse, g.player) for g in game_players.items],
        "total": game_players.total,
        "limit": limit,
        "offset": offset,
    }


async def get_game_id(session, id):
    game = await check_game_by_id(session, id)

    return to_schema(GameResponse, game)


async def create_game(session, item, user_id):
    new_game = await add_game(session, item, user_id)

    return to_schema(BaseShortResponse, new_game)


async def change_game(session, id, item, user_id):
    game = await check_game_by_id(session, id)

    if game.organizer_id != user_id:
        raise ApplicationException("Only organizer can change game", 400)

    update_data = item.model_dump(exclude_unset=True)

    start_time = update_data.get("start_time", None) or game.start_time

    if start_time:
        if start_time < datetime.now():
            raise ApplicationException("Cannot start game earlier than now", 400)

    for name, value in update_data.items():
        setattr(game, name, value)

    return to_schema(GameResponse, game)


async def join_game(session, game_id, player_id):
    await check_game_by_id(session, game_id)

    in_game = await is_player_in_game(session, player_id, game_id)

    if in_game.status == Status.JOINED:
        existing = await get_active_player_table(session, player_id, game_id)

        if existing:
            raise ApplicationException(
                f"Player already joined table number {existing.table.number}_{existing.table.id}",
                400,
            )

    if in_game.status == Status.LEFT:
        in_game.status = Status.JOINED
        return {"result": "joined"}

    await add_to_game(session=session, game_id=game_id, player_id=player_id)

    return {"result": "joined"}


async def leave_game(session, game_id, player_id):
    await check_game_by_id(session, game_id)

    in_game = await is_player_in_game(session, player_id, game_id)

    if not in_game:
        raise ApplicationException("Player is not in the game", 400)

    else:
        existing = await get_active_player_table(session, player_id, game_id)

        if existing:
            raise ApplicationException(
                f"To leave game please leave table {existing.table.number}_{existing.table.id}", 400
            )

    in_game.status = Status.LEFT

    return {"result": "left"}


async def archive_game(session, id, user_id):
    game = await get_game_by_id(session, id)

    if not game:
        raise ApplicationException("Game not found", 404)

    if game.organizer_id != user_id:
        raise ApplicationException("Only organizer can archive game", 400)

    if game.is_archived:
        raise ApplicationException(f"Game {game.name} is archived", 400)

    game.is_archived = True
    return game


async def restore_game(session, id, user_id):
    game = await get_game_by_id(session, id)

    if not game:
        raise ApplicationException("Game not found", 404)

    if game.organizer_id != user_id:
        raise ApplicationException("Only organizer can change game", 400)

    if not game.is_archived:
        raise ApplicationException("Game is already active", 400)

    game.is_archived = False
    return game


async def distribute_tables(session, game_id, user_id):
    game = await check_game_by_id(session, game_id)

    if game.organizer_id != user_id:
        raise ApplicationException("Only organizer can distribute tables", 400)

    tables = game.tables
    if not tables:
        round_number = 1
    else:
        if any(t.finished_at is None for t in tables):
            raise ApplicationException("There are active tables, cannot start new round", 400)
        round_number = max(t.round for t in tables) + 1

    game.start_time = datetime.utcnow()
    game.status = GameStatus.IN_ACTION

    # count tables logic:
    players_number = await get_game_players_count(session, game_id)
    tables_number = 0  # total tables

    # create tables logic:
    new_tables = await add_tables(session=session, game_id=game_id, item=tables_number)

    # getting game players by rating:
    sorting = {"elo": ("elo",)}
    players = await get_game_players(
        session=session, game_id=game_id, limit=100, offset=0, sort="-elo", sorting_rules=sorting
    )

    # distribute table logic

    return await build_distribute_response(game, new_tables)


async def build_distribute_response(game, tables):
    result_tables = []

    for table in tables:
        players = []

        for tp in table.table_participants:
            p = tp.player

            players.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "telegram_id": p.telegram_id,
                }
            )

        result_tables.append(
            {
                "id": table.id,
                "number": table.number,
                "round": table.round,
                "players": players,
            }
        )

    return {
        "game_id": game.id,
        "tables": result_tables,
    }
