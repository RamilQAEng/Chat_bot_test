from aiogram import Router, types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Создаем роутер для клавиатур
keyboard_router = Router()

# Создаем клавиатуру с основными кнопками
main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 Отправить ТЗ", callback_data="send_tz")],
        [InlineKeyboardButton(text="🆕 Новая сессия", callback_data="new_session")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ]
)

@keyboard_router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=main_keyboard)

@keyboard_router.callback_query(lambda c: c.data == "send_tz")
async def send_tz_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Пожалуйста, отправьте текст или документ с ТЗ. Я сгенерирую отчет.")
    # Устанавливаем состояние ожидания ТЗ
    await state.set_state("waiting_for_tz")
    # Сохраняем информацию о том, что пользователь нажал кнопку
    await state.update_data(waiting_for_tz=True)
    await callback.answer()

@keyboard_router.callback_query(lambda c: c.data == "new_session")
async def new_session_handler(callback: types.CallbackQuery):
    # Здесь будет логика сброса сессии
    await callback.message.answer("Новая сессия начата. Все предыдущие данные сброшены.")
    await callback.answer()

@keyboard_router.callback_query(lambda c: c.data == "help")
async def help_handler(callback: types.CallbackQuery):
    help_text = """
🤖 О боте:
Этот бот помогает автоматизировать создание тест-кейсов на основе технического задания. Он использует искусственный интеллект для анализа ТЗ и генерации тестовых сценариев.

📋 Основные функции:
1. Автоматическая генерация тест-кейсов
2. Сохранение результатов в базу данных
3. Экспорт тест-кейсов в Excel
4. Управление сессиями тестирования

📌 Доступные команды:
📝 Отправить ТЗ - загрузите текст или документ с техническим заданием
🆕 Новая сессия - начать новую сессию тестирования
ℹ️ Помощь - показать это сообщение

После получения Excel-файла вы автоматически вернетесь в главное меню для продолжения работы.
"""
    await callback.message.answer(help_text)
    await callback.answer()

def register_keyboards(dp: Dispatcher):
    """Регистрация всех клавиатур"""
    dp.include_router(keyboard_router)
