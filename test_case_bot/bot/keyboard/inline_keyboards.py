from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Отправить ТЗ")],
            [KeyboardButton(text="🆕 Новая сессия")],
            [KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True,  # Уменьшаем размер кнопок
        persistent=True  # Делаем клавиатуру постоянной
    )

