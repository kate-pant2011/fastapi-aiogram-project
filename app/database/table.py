from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .common import apply_sorting, get_all_and_total
from app.models.table import Table
from app.models.game import Game
from app.models.table_player import TablePlayer


async def get_all_tables(session, limit, offset, game_id, sorting_rules):
    stmt = select(Table).where(Table.game_id == game_id).where(Table.finished_at.is_(None))

    stmt = apply_sorting(stmt=stmt, model=Table, sort="number", sorting_rules=sorting_rules)

    result = await get_all_and_total(session, stmt, limit, offset)
    return result


async def get_table_by_id(session, table_id):
    result = await session.execute(
        select(Table)
        .options(selectinload(Table.table_participants).selectinload(TablePlayer.player))
        .options(selectinload(Table.game))
        .where(Table.id == table_id)
    )
    table = result.scalar_one_or_none()
    return table


async def add_tables(session, game_id, item):
    for num in range(item.total_tables):
        table = Table(number=num + 1, round=item.round, game_id=game_id)

        session.add(table)

    await session.flush()
