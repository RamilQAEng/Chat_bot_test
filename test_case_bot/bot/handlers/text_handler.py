from aiogram import types
from aiogram.fsm.context import FSMContext
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
        
        # Сохранение в базу данных
        db = DatabaseClient()
        db.connect()
        
        for line in response.split("\n"):
            if "|" in line:
                title, precond, steps, result, priority = line.split("|")
                test_case = TestCase(
                    title=title.strip(),
                    preconditions=precond.strip(),
                    steps=steps.strip(),
                    expected_result=result.strip(),
                    priority=priority.strip()
                )
                db.save_test_case(test_case)
        
        db.close()
        
        # Создание Excel-файла
        excel_file = create_excel_from_test_cases(response)
        await message.answer_document(types.FSInputFile(excel_file), caption="✅ Готово! Вот тест-кейсы.")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке ТЗ.")

def register_handlers(dp):
    dp.message.register(process_text_tz, lambda msg: msg.text and not msg.text.startswith('/'))