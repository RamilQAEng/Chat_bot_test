from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from services.gigachat_service import GigaChatService
from services.excel_service import create_excel_from_test_cases
from database.db_client import DatabaseClient
from models.test_case import TestCase
import logging

gigachat = GigaChatService()

async def process_text_tz(message: types.Message):
    await message.answer("⏳ Обрабатываю текст...")
    
    try:
        response = await gigachat.generate_test_cases(message.text)
        if not response:
            return await message.answer("❌ Ошибка генерации")
            
        # Сохраняем в БД
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
        
        # Создаем Excel
        excel_file = create_excel_from_test_cases(response)
        await message.answer_document(types.FSInputFile(excel_file))
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.answer("⚠️ Произошла ошибка")

def register_handlers(dp: Dispatcher):
    dp.message.register(process_text_tz, lambda msg: msg.text and not msg.text.startswith('/'))