from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Отправить ТЗ", callback_data="send_tz")],
        [InlineKeyboardButton(text="🆕 Новая сессия", callback_data="new_session")],
        [InlineKeyboardButton(text="ℹ️ Помощь", callback_data="help")]
    ])

