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
        reply_markup=get_main_keyboard()  # Показываем клавиатуру с кнопками
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
        "Команды:\n"
        "/start - Начать\n"
        "/help - Справка\n"
        "/new - Новая сессия"
    )

# Обработчик команды /new
async def cmd_new(message: types.Message, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    logger.info("Обработка команды /new")
    await message.answer("🆕 Новая сессия начата. Отправьте мне ТЗ.")

# Регистрация обработчиков команд
def register_handlers(dp):
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_new, Command("new"))