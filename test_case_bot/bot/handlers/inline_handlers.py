from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.logger import logger
from bot.handlers.states import UserStates  # Импортируем состояние

# Обработчик для кнопки "Отправить ТЗ"
async def handle_send_tz_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки "Отправить ТЗ".
    Переводит бота в состояние ожидания текста.
    """
    logger.info("Обработка кнопки 'Отправить ТЗ'")
    await state.set_state(UserStates.waiting_for_tz)  # Переводим бота в состояние ожидания ТЗ
    await callback.message.answer("📝 Отправьте ТЗ текстом.")
    await callback.answer()  # Завершаем callback

# Обработчик для кнопки "Помощь"
async def handle_help_callback(callback: types.CallbackQuery):
    """
    Обрабатывает нажатие кнопки "Помощь".
    Отправляет инструкцию по использованию бота.
    """
    logger.info("Обработка кнопки 'Помощь'")
    await callback.message.answer(
        "📚 Как использовать бота:\n"
        "1. Нажмите кнопку 'Отправить ТЗ'.\n"
        "2. Отправьте ТЗ текстом.\n"
        "3. Дождитесь обработки.\n"
        "4. Получите Excel-файл с тест-кейсами.\n\n"
        "Команды:\n"
        "/start - Начать\n"
        "/help - Справка\n"
        "/new - Новая сессия"
    )
    await callback.answer()  # Завершаем callback

# Обработчик для кнопки "Новая сессия"
async def handle_new_session_callback(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки "Новая сессия".
    Сбрасывает состояние и начинает новую сессию.
    """
    logger.info("Обработка кнопки 'Новая сессия'")
    await state.clear()  # Сбрасываем состояние
    await callback.message.answer("🆕 Новая сессия начата. Нажмите 'Отправить ТЗ', чтобы начать.")
    await callback.answer()

# Регистрация обработчиков
def register_handlers(dp):
    """
    Регистрирует обработчики для inline-кнопок.
    """
    dp.callback_query.register(handle_send_tz_callback, lambda c: c.data == "send_tz")
    dp.callback_query.register(handle_help_callback, lambda c: c.data == "help")
    dp.callback_query.register(handle_new_session_callback, lambda c: c.data == "new_session")