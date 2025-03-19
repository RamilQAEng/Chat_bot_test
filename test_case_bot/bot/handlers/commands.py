from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.logger import logger
from bot.keyboard.inline_keyboards import get_main_keyboard

# Обработчик команды /start
async def cmd_start(message: types.Message):
    logger.info("Обработка команды /start")
    await message.answer(
        "👋 Привет! Я помогу сгенерировать тест-кейсы. Выберите действие:",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /help
async def cmd_help(message: types.Message, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    logger.info("Обработка команды /help")
    await message.answer(
        "📚 Как использовать бота:\n"
        "1. Отправьте ТЗ в виде текста или файла.\n"
        "2. Дождитесь обработки.\n"
        "3. Получите Excel-файл с тест-кейсами.\n\n"
        "Доступные кнопки:\n"
        "📝 Отправить ТЗ - Отправить новое ТЗ\n"
        "🆕 Новая сессия - Начать новую сессию\n"
        "ℹ️ Помощь - Показать эту справку",
        reply_markup=get_main_keyboard()
    )

# Обработчик команды /new
async def cmd_new(message: types.Message, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    logger.info("Обработка команды /new")
    await message.answer(
        "🆕 Новая сессия начата. Отправьте мне ТЗ.",
        reply_markup=get_main_keyboard()
    )

# Регистрация обработчиков команд
def register_handlers(dp):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_new, Command("new"))