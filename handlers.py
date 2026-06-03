from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from ai_client import get_ai_response
from config import MAX_HISTORY_MESSAGES

router = Router()

# Хранилище истории диалогов: {user_id: [{"role": ..., "content": ...}]}
dialog_history: dict[int, list[dict]] = {}


@router.message(CommandStart())
async def cmd_start(message: Message):
    dialog_history.pop(message.from_user.id, None)
    await message.answer(
        "Привет! Я ассистент компании «Центр Красок».\n"
        "Спрашивайте о наших товарах, услугах, адресах и всём остальном — я помогу."
    )


@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text.strip()

    if not user_text:
        return

    history = dialog_history.setdefault(user_id, [])
    history.append({"role": "user", "content": user_text})

    # Обрезаем историю, чтобы не раздувать контекст
    if len(history) > MAX_HISTORY_MESSAGES:
        dialog_history[user_id] = history[-MAX_HISTORY_MESSAGES:]
        history = dialog_history[user_id]

    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        reply = await get_ai_response(history)
    except Exception as e:
        reply = "Произошла ошибка при обращении к AI. Попробуйте позже."
        print(f"AI error for user {user_id}: {e}")

    history.append({"role": "assistant", "content": reply})
    await message.answer(reply)
