import logging
from aiogram import types
from services.gigachat_service import generate_response

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def handle_document(message: types.Message):
    document = message.document
    if document.mime_type == "text/plain":
        # Скачиваем документ
        file = await document.get_file()
        file_path = file.file_path
        await document.download(destination_file="temp_file.txt")
        
        # Читаем содержимое файла
        with open("temp_file.txt", "r", encoding="utf-8") as f:
            text = f.read()
        
        # Генерация ответа через GIGA CHAT API
        try:
            response = generate_response(text)
            await message.reply(response)
        except Exception as e:
            logging.error(f"Ошибка при генерации ответа: {e}")
            await message.reply("Произошла ошибка при обработке вашего документа. Пожалуйста, попробуйте позже.")
    else:
        await message.reply("Пожалуйста, отправьте текстовый файл (.txt).")