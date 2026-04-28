from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .common import get_all_and_total
from app.models.tgchat import TelegramChat


async def get_all_tgchats(session, limit, offset):
    stmt = select(TelegramChat)

    stmt.order_by(TelegramChat.created_at.desc(), TelegramChat.chat_id.desc())

    result = await get_all_and_total(session, stmt, limit, offset)
    return result


async def get_tgchat_by_chat_id(session, chat_id):
    result = await session.execute(
        select(TelegramChat)
        .options(selectinload(TelegramChat.activator))
        .options(selectinload(TelegramChat.games))
        .where(TelegramChat.chat_id == chat_id)
    )
    tgchat = result.scalar_one_or_none()
    return tgchat


async def add_tgchat(session, item, user_id):
    tgchat = TelegramChat(
        chat_id=item.chat_id,
        thread_id=item.thread_id,
        chat_title=item.chat_title,
        activator_id=user_id
    )

    session.add(tgchat)
    await session.flush()
    return tgchat