import asyncio
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from bot.handlers.text_handler import register_handlers as register_text_handlers
from bot.handlers.document_handler import register_handlers as register_document_handlers
from bot.keyboard.inline_keyboards import register_keyboards
from bot.handlers.text_handler import start_command

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем клавиатуры
    register_keyboards(dp)
    
    # Регистрируем обработчики
    register_text_handlers(dp)
    register_document_handlers(dp)
    

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
