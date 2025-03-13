from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.logger import logger
from bot.keyboard.inline_keyboards import get_main_keyboard

# Обработчик для кнопки "Старт"
async def handle_start_callback(callback: types.CallbackQuery):
    logger.info("Обработка кнопки 'Старт'")
    await callback.message.answer(
        "👋 Привет! Я помогу сгенерировать тест-кейсы. Выберите действие:",
        reply_markup=get_main_keyboard()  # Показываем клавиатуру с кнопками
    )
    await callback.answer()  # Завершаем callback

# Обработчик для кнопки "Помощь"
async def handle_help_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    logger.info("Обработка кнопки 'Помощь'")
    await callback.message.answer(
        "📚 Как использовать бота:\n"
        "1. Отправьте ТЗ в виде текста или файла.\n"
        "2. Дождитесь обработки.\n"
        "3. Получите Excel-файл с тест-кейсами.\n\n"
        "Команды:\n"
        "/start - Начать\n"
        "/help - Справка\n"
        "/new - Новая сессия"
    )
    await callback.answer()

# Обработчик для кнопки "Новая сессия"
async def handle_new_session_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()  # Сбрасываем состояние
    logger.info("Обработка кнопки 'Новая сессия'")
    await callback.message.answer("🆕 Новая сессия начата. Отправьте мне ТЗ.")
    await callback.answer()

# Регистрация обработчиков
def register_handlers(dp):
    dp.callback_query.register(handle_start_callback, lambda c: c.data == "start")
    dp.callback_query.register(handle_help_callback, lambda c: c.data == "help")
    dp.callback_query.register(handle_new_session_callback, lambda c: c.data == "new_session")