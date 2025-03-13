import asyncio
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from bot.handlers.commands import register_handlers as register_command_handlers
from bot.handlers.inline_handlers import register_handlers as register_inline_handlers
from bot.handlers.text_handler import register_handlers as register_text_handlers

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем обработчики команд и inline-кнопок
    register_command_handlers(dp)
    register_inline_handlers(dp)
    register_text_handlers(dp)  # Добавляем регистрацию обработчика текстовых сообщений

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронного event loop