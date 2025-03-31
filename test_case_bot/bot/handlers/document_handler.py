from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.logger import logger
from services.gigachat_service import GigaChatService
from services.excel_service import create_excel_from_test_cases
from database.db_client import DatabaseClient
from models.test_case import TestCase
from bot.keyboard.inline_keyboards import main_keyboard
import os
import docx
import asyncio

gigachat = GigaChatService()

async def process_document_tz(message: types.Message, state: FSMContext):
    logger.info("Обработка документа ТЗ")
    await message.answer("⏳ Обрабатываю документ...")
    
    try:
        # Проверяем, находится ли пользователь в состоянии ожидания ТЗ
        data = await state.get_data()
        if not data.get('waiting_for_tz'):
            return
        
        # Скачиваем документ
        file = await message.bot.get_file(message.document.file_id)
        file_path = file.file_path
        
        # Сохраняем временный файл
        temp_file = f"temp_{message.document.file_name}"
        await message.bot.download_file(file_path, temp_file)
        
        # Проверяем формат файла
        if not message.document.file_name.endswith('.docx'):
            return await message.answer("❌ Поддерживаются только файлы формата .docx")
        
        # Читаем docx файл
        doc = docx.Document(temp_file)
        doc_text = "\n".join([para.text for para in doc.paragraphs])
        
        # Логируем содержимое документа
        logger.info(f"Содержимое документа:\n{doc_text[:1000]}...")  # Логируем первые 1000 символов
        
        # Ищем раздел с функциональными требованиями
        start_markers = [
            'функциональные требования',
            'functional requirements',
            'функционал',
            'функции'
        ]
        
        # Находим начало раздела
        start_index = -1
        for marker in start_markers:
            start_index = doc_text.lower().find(marker)
            if start_index != -1:
                break
                
        if start_index == -1:
            return await message.answer("❌ В документе не найден раздел с функциональными требованиями.")
        
        # Берем текст после найденного маркера (максимум 10000 символов)
        functional_reqs = doc_text[start_index:start_index+10000]
        logger.info(f"Найден раздел функциональных требований: {functional_reqs[:500]}...")
        
        if len(functional_reqs) >= 10000:
            logger.warning("Раздел функциональных требований превышает 10000 символов. Будут обработаны только первые 10000 символов.")
        
        # Удаляем временный файл
        os.remove(temp_file)
        
        if not functional_reqs:
            return await message.answer("❌ В документе не найдены функциональные требования.")
        
        # Разделяем текст на части по 5000 символов
        chunk_size = 5000
        chunks = [functional_reqs[i:i+chunk_size] for i in range(0, len(functional_reqs), chunk_size)]
        
        all_test_cases = []
        
        # Обрабатываем каждую часть
        for i, chunk in enumerate(chunks):
            logger.info(f"Обработка части {i+1} из {len(chunks)}")
            
            # Генерация тест-кейсов
            response = await gigachat.generate_test_cases(chunk)
            
            if not response:
                return await message.answer(f"❌ Ошибка: сервис GigaChat не вернул данные для части {i+1}.")
            
            # Парсим JSON ответ
            test_cases = gigachat.parse_json_response(response)
            all_test_cases.extend(test_cases)
            
            # Пауза между запросами
            await asyncio.sleep(1)
        
        test_cases = all_test_cases
        
        if not test_cases:
            return await message.answer("❌ Не удалось сгенерировать тест-кейсы. Проверьте формат функциональных требований.")
        
        # Создание Excel-файла
        try:
            excel_file = create_excel_from_test_cases(test_cases)
            await message.answer_document(types.FSInputFile(excel_file), caption="✅ Готово! Вот тест-кейсы.")
        except Exception as e:
            logger.error(f"Ошибка при создании Excel файла: {e}")
            return await message.answer("❌ Произошла ошибка при создании Excel файла.")
        
        # Возвращаем пользователя в главное меню
        await message.answer("Выберите следующее действие:", reply_markup=main_keyboard)
        
        # Сбрасываем состояние
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await message.answer("⚠️ Произошла ошибка при обработке документа.")
        await state.clear()

def register_handlers(dp):
    dp.message.register(process_document_tz, lambda msg: msg.document)
