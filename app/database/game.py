from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from .common import order, get_all_and_total, apply_sorting
from app.models.game import Game, GamePlayer, Status, GameStatus
from app.models.player import Player
from app.models.table import Table
from app.models.table_player import TablePlayer


async def get_all_games(session, limit, offset, status, organizer_id):
    stmt = select(Game).where(Game.is_archived.is_(False))

    if organizer_id is not None:
        stmt = stmt.where(Game.organizer_id == organizer_id)

    if status is not None:
        stmt = stmt.where(Game.status == status)

    stmt = order(stmt=stmt, model=Game)

    result = await get_all_and_total(session, stmt, limit, offset)
    return result

async def get_active_game(session):
    stmt = await session.execute(
        select(Game)
        .where(Game.is_archived.is_(False))
        .where(Game.status == GameStatus.IN_ACTION)
    )
    game = stmt.scalars.first()
    return game

async def get_game_players(
        session, game_id, limit, offset, sort=None, sorting_rules=None
):
    stmt = (
    select(GamePlayer)
    .options(selectinload(GamePlayer.player))
    .where(GamePlayer.status == Status.JOINED)
    .where(GamePlayer.game_id == game_id)
    )

    if sorting_rules:
        stmt =  apply_sorting(stmt=stmt, model=Player, sort=sort, sorting_rules=sorting_rules)
    
    else:
        stmt = order(stmt=stmt, model=GamePlayer)

    result = await get_all_and_total(session, stmt, limit, offset)

    return result


async def get_game_by_id(session, id):
    result = await session.execute(
        select(Game)
        .options(selectinload(Game.players))
        .options(selectinload(Game.tables).selectinload(Table.table_participants).selectinload(TablePlayer.player))
        .options(selectinload(Game.organizer))
        .where(Game.id == id)
    )
    game = result.scalar_one_or_none()
    return game


async def is_player_in_game(session, player_id, game_id):
    result = await session.execute(
    select(GamePlayer)
    .options(selectinload(GamePlayer.player))
    .where(GamePlayer.game_id == game_id)
    .where(GamePlayer.player_id == player_id)
    )

    result = result.scalar_one_or_none()

    return result


async def add_game(session, item, user_id):
    game = Game(
        name=item.name,
        start_time=item.start_game,
        organizer_id=user_id
    )
    session.add(game)
    await session.flush()
    return game


async def add_to_game(session, player_id, game_id):
    game_player = GamePlayer(
        player_id=player_id,
        game_id=game_id,
    )

    session.add(game_player)
    await session.flush()
    return game_player


async def get_game_players_count(session, game_id):
    result = await session.execute(
        select(func.count(GamePlayer.id))
        .where(GamePlayer.game_id == game_id)
        .where(GamePlayer.status == Status.JOINED)
    )
    return result.scalar() or 0