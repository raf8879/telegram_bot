import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_BOT_TOKEN, logger
from handlers.start import router as start_router
from handlers.contact import router as contact_router
from handlers.pronunciation import router as pronunciation_router
from handlers.conversation import router as conversation_router
from handlers.image_generation import router as image_router
from handlers.text_chat import router as text_chat_router
from handlers.commands import router as commands_router

from services.analytics import load_analytics
from services.detailed_analytics import load_detailed_analytics
from datetime import datetime, timedelta
import asyncio


user_last_activity = {}

async def clear_user_context(dp: Dispatcher):
    """
    Каждые n секунд проверять неактивных пользователей и очищать состояние.
    """
    while True:
        current_time = datetime.now()
        for user_id, last_active in list(user_last_activity.items()):
            if current_time - last_active > timedelta(minutes=15):
                await dp.fsm.storage.clear_state(chat_id=user_id, user_id=user_id)
                logger.info(f"Контекст пользователя {user_id} очищен из-за неактивности.")
                del user_last_activity[user_id]
        await asyncio.sleep(60)

async def set_bot_commands(bot: Bot):
    from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="contact", description="Связаться с владельцем"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())


    from config import OWNER_ID
    private_commands = commands + [
        BotCommand(command="analytics_1", description="Базовая аналитика"),
        BotCommand(command="analytics_2", description="Детализированная аналитика"),
    ]
    await bot.set_my_commands(private_commands, scope=BotCommandScopeChat(chat_id=OWNER_ID))

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())


    dp.include_router(start_router)
    dp.include_router(contact_router)
    dp.include_router(pronunciation_router)
    dp.include_router(conversation_router)
    dp.include_router(image_router)
    dp.include_router(text_chat_router)
    dp.include_router(commands_router)

    await set_bot_commands(bot)


    asyncio.create_task(clear_user_context(dp))


    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
