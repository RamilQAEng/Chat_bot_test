from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.logger import logger

# Обработчик для кнопки "Помощь"
async def handle_help_callback(callback: types.CallbackQuery):
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
    await callback.answer()  # Завершаем callback

# Обработчик для кнопки "Новая сессия"
async def handle_new_session_callback(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Обработка кнопки 'Новая сессия'")
    await state.clear()  # Сбрасываем состояние
    await callback.message.answer("🆕 Новая сессия начата. Отправьте мне ТЗ.")
    await callback.answer()

# Обработчик для кнопки "Отправить ТЗ"
async def handle_send_tz_callback(callback: types.CallbackQuery, state: FSMContext):
    logger.info("Обработка кнопки 'Отправить ТЗ'")
    await callback.message.answer("📝 Отправьте ТЗ текстом или файлом.")
    await state.set_state("waiting_for_tz")  # Устанавливаем состояние ожидания ТЗ
    await callback.answer()

# Регистрация обработчиков
def register_handlers(dp):
    dp.callback_query.register(handle_help_callback, lambda c: c.data == "help")
    dp.callback_query.register(handle_new_session_callback, lambda c: c.data == "new_session")
    dp.callback_query.register(handle_send_tz_callback, lambda c: c.data == "send_tz")