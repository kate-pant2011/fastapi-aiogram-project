from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.api.player import get_leaderboard
from bot.utils.formatting import leaderboard_text
from bot.api.table import get_tables
from bot.config import APIError

router = Router(name="common")


@router.message(Command("rating"))
async def cmd_rating(message: Message):
    user = message.from_user
    if not user:
        return
    
    try:
        data = await get_leaderboard(tg_id=user.id)

    except APIError as e:
        await message.answer(f"⚠️ {e.message}")
        return

    items = data.get("items", [])

    text = leaderboard_text(items)

    await message.answer(text)


@router.message(Command("tables"))
async def cmd_tables(message: Message):
    try:
        data = await get_tables()
    except Exception:
        await message.answer("❌ Cannot load tables")
        return

    tables = data.get("tables", [])

    if not tables:
        await message.answer("❌ No active tables")
        return

    text = "🃏 <b>Tables</b>\n\n"

    for t in tables:
        text += f"🟢 <b>Table {t['number']}</b> — {t['players_alive']}/{t['players_total']} alive\n"

        for p in t["players"]:
            mark = "" if p["is_alive"] else " ❌"
            text += f"  {p['name']}{mark}\n"

        text += "\n"

    await message.answer(text)


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "<b>🃏 Poker Bot Commands</b>\n\n"

        "<b>👤 Registration</b>\n"
        "/register — create your profile\n\n"

        "<b>🎮 Game</b>\n"
        "/join — join current game\n"
        "/leave — leave game\n"
        "/start — start game (organizer only)\n\n"

        "<b>📊 Stats</b>\n"
        "/rating — leaderboard (top players)\n"
        "/stats — your personal stats\n\n"

        "<b>🪑 Table actions</b>\n"
        "/chips — set chips for players at your table\n"
        "/knockout — mark who you knocked out\n"
        "/finish — close table & calculate results (organizer only)\n\n"

        "<b>ℹ️ Other</b>\n"
        "/help — show this message\n"
    )

    await message.answer(text)