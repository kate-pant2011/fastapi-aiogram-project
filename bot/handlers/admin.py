from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message,  CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from bot.api.game import get_my_games_api, distribute_tables_api, get_game_in_action
from bot.api.table import get_tables, close_table
from bot.utils.formatting import format_table_result
from bot.utils.broadcast import broadcast_table_results
from bot.config import APIError

from bot.states.register import RegisterState

router = Router()


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await message.answer("Nice to meet you! Please add your nickname:")

    await state.set_state(RegisterState.waiting_for_name)


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = message.from_user
    if not user:
        return

    try:
        games = await get_my_games_api(tg_id=user.id, organizer_id=user.id)

    except APIError as e:
        await message.answer(f"⚠️ {e.message}")
        return
    
    items = games.get("items", [])
    if not items:
        await message.answer("❌ No awaited games")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Game #{g['id']}",
                    callback_data=f"start_game:{g['id']}"
                )
            ]
            for g in games["items"]
        ]
    )

    await message.answer("🎮 Choose game to start:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("start_game:"))
async def cb_start_game(callback: CallbackQuery):
    user = callback.from_user
    if not user:
        return

    game_id = int(callback.data.split(":")[1])

    try:
        data = await distribute_tables_api(
            game_id=game_id,
            tg_id=user.id
        )
    except APIError as e:
        await callback.answer(e.message, show_alert=True)
        return

  
    text = [f"🎮 Game #{game_id} started!\n"]

    for table in data["tables"]:
        text.append(f"Table {table['number']}:")
        for p in table["players"]:
            text.append(f" - {p['name']}")
        text.append("")

    try:
        await callback.message.edit_text("\n".join(text))
    except Exception:
        pass
    
    for table in data["tables"]:
        for p in table["players"]:
            try:
                await callback.bot.send_message(
                    chat_id=p["telegram_id"],
                    text=f"🪑 You are seated at table {table['table_number']}"
                )
            except Exception:
                pass

    await callback.answer()


@router.message(Command("finish"))
async def cmd_finish(message: Message):
    user = message.from_user
    if not user:
        return

    try:
        games = await get_game_in_action(tg_id=user.id)
        games = games["items"] or []

        if not games:
            await message.answer("❌ No active game")
            return
        
        if len(games) > 1:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text=f"Game #{g['name']}",
                            callback_data=f"finish_game:{g['id']}"
                        )
                    ]
                    for g in games
                ]
            )

            await message.answer("🎮 Choose game:", reply_markup=keyboard)
            return
        
        game = games[0]

        tables = await get_tables(
            tg_id=user.id,
            game_id=game["id"]
        )

        if not tables.get("items"):
            await message.answer("❌ No tables available")
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Table {t['number']} ({t['table_participants']} players)",
                        callback_data=f"close_table:{t['id']}"
                    )
                ]
                for t in tables["items"]
            ]
        )

        await message.answer(
            "🪑 Choose table to finish:",
            reply_markup=keyboard
        )

    except APIError as e:
        await message.answer(f"⚠️ {e.message}")
        return


@router.callback_query(F.data.startswith("finish_game:"))
async def cb_finish_game(callback: CallbackQuery):
    user = callback.from_user
    if not user:
        return

    game_id = int(callback.data.split(":")[1])

    try:
        tables = await get_tables(
            tg_id=user.id,
            game_id=game_id
        )

        items = tables.get("items", [])

        if not items:
            await callback.answer("❌ No tables available", show_alert=True)
            return

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"Table {t['number']} ({t.get('table_participants', '?')} players)",
                        callback_data=f"close_table:{t['id']}"
                    )
                ]
                for t in items
            ]
        )

        await callback.message.edit_text(
            "🪑 Choose table to finish:",
            reply_markup=keyboard
        )

        await callback.answer()

    except APIError as e:
        await callback.answer(f"⚠️ {e.message}", show_alert=True)

    except Exception:
        await callback.answer("🚫 Server error", show_alert=True)
       


@router.callback_query(F.data.startswith("close_table:"))
async def cb_close_table(callback: CallbackQuery):
    user = callback.from_user
    if not user:
        return

    table_id = int(callback.data.split(":")[1])

    try:
        result = await close_table(
            tg_id=user.id,
            table_id=table_id
        )
    except APIError as e:
        await callback.answer(e.message, show_alert=True)
        return
    
    except Exception as e:
        await callback.answer(str(e), show_alert=True)
        return

    text = format_table_result(result)

    await callback.message.edit_text(text)

    await broadcast_table_results(callback.bot, result)

    await callback.answer()
