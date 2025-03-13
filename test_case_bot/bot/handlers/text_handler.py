from aiogram import types
from aiogram.fsm.context import FSMContext
from pydantic import ValidationError
from services.gigachat_service import GigaChatService
from services.excel_service import create_excel_from_test_cases
from database.db_client import DatabaseClient
from models.test_case import TestCase
from utils.logger import logger


gigachat = GigaChatService()

async def process_text_tz(message: types.Message, state: FSMContext):
    logger.info("Обработка текстового ТЗ")
    await message.answer("⏳ Обрабатываю текст...")
    
    try:
        # Генерация тест-кейсов
        response = await gigachat.generate_test_cases(message.text)
        if not response:
            return await message.answer("❌ Ошибка генерации тест-кейсов.")
        
        # Парсинг тест-кейсов
        test_cases = GigaChatService.parse_test_cases(response)
        if not test_cases:
            return await message.answer("❌ Не удалось распарсить тест-кейсы.")
        
        # Подключение к базе данных
        db = DatabaseClient()
        db.connect()
        
        # Сохранение тест-кейсов в базу данных
        for test_case_data in test_cases:
            try:
                test_case = TestCase(**test_case_data)
                db.save_test_case(test_case)
            except ValidationError as e:
                logger.error(f"❌ Ошибка валидации тест-кейса: {e}")
                continue
        
        # Закрытие соединения с базой данных
        db.close()
        
        # Создание Excel-файла
        excel_file = create_excel_from_test_cases(response)
        await message.answer_document(types.FSInputFile(excel_file), caption="✅ Готово! Вот тест-кейсы.")
        
        # Сбрасываем состояние
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке ТЗ.")
        await state.clear()

def register_handlers(dp):
    dp.message.register(process_text_tz, lambda msg: msg.text and not msg.text.startswith('/'))